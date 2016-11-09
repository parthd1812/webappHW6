
# @author Parth Desai
# parthd@andrew.cmu.edu


from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *
from grumblr.models import Bio


from grumblr.forms import *
from django.db import models

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from mimetypes import guess_type
from grumblr.validators import validate_file_extension
from django.core import serializers
from django.http import HttpResponse

#----------------Saves user data on new signup and send an email-------------------------#
def signup(request):
    context = {}
    if request.method =='GET':
       context['form'] = Signup()
       return render(request,'grumblr/signup.html', context)

    form = Signup(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/signup.html', context)
    username = request.POST["username"]
    new_user = User.objects.create_user(username=username, password=form.cleaned_data['password1'], email=form.cleaned_data['email'], first_name=form.cleaned_data['first'], last_name=form.cleaned_data['last'])
    new_user.save()
    user = User.objects.get(username= username)
    emailAddress=user.email
    username = user.username
    user.is_active = False
    user.save()
    token = default_token_generator.make_token(user)
    email_body = """Please click on the link below confirm you account

    http://%s%s"""%(request.get_host(), reverse('emailconfirm', args=(username, token)))     
    send_mail(subject = "grumblr Registeration Confirmation", message = email_body, from_email = "desaiparth1812@gmail.com", recipient_list =[user.email])
    user = User.objects.get(username= request.POST['username'])
    new_user = authenticate(username=request.POST['username'], password = form.cleaned_data['password1'])
    if new_user is not None:
        login(request, new_user)
    bio = Bio(short_bio= "Hi there I am using grumblr", age="999",  user=user, token=token)
    bio.save()
    context['message'] = "Congratulations! Registeration Succesful. Please Confirm the link !"
    return render(request,'grumblr/signup.html', context)

#----------------Adds new post to the database-------------------
@login_required
def globalpage(request):
    context ={}
    allpost=Post.objects.all()
    documents = Document.objects.all();
    allcomments = Comments.objects.all();
    context = {'allpost': allpost, 'documents':documents, 'allcomments':allcomments}
    if request.method =='GET':
       context['form'] = Globalpage()
       context['form1'] = Comment()
       return render(request,'grumblr/globalpage.html', context)
    form = Globalpage(request.POST)
    context['form'] = form
    form1 = Comment(request.POST)
    context['form1'] = form1
    if not form.is_valid ():
        return render(request, 'grumblr/globalpage.html', context)
    if (request.method =='POST'):
        if form.cleaned_data['post']:
            new_item = Post(text = form.cleaned_data['post'], user=request.user)
            new_item.save()
    context['form'] = Globalpage()
    context['form1'] = Comment()
    return render(request,'grumblr/globalpage.html', context)
 

#---------------Follower page implementation with toggling buttons---------------
@login_required
def profile(request):
    context = {}

    if (request.method =='GET'):
        user = request.user
    else: 
        if 'profile' in request.POST:
            user = User.objects.get(username=str(request.POST['profile']))

        if 'follow' in request.POST:
            user = User.objects.get(username=request.POST['follow'])

        if 'unfollow' in request.POST:
            user = User.objects.get(username=request.POST['unfollow'])

    userinfo =User.objects.get(username=user)
    posts=Post.objects.filter(user=userinfo)
    documents = Document.objects.all()
    bio = Bio.objects.get(user=userinfo)
    allcomments = Comments.objects.all()
    image_user = Document.objects.filter(user=userinfo)

    if documents:
        context ={'items':posts,'user':user, 'documents':documents, 'bio':bio, 'allcomments':allcomments,'image_user':image_user}
    else:
        context ={'items':posts,'user':user, 'bio':bio,'allcomments':allcomments, 'documents': documents,'image_user':image_user}



    def buttonchecker():
        bio_user = Bio.objects.get(user=request.user)
        if bio_user:
            bio_user = bio_user.following.all()
            for bio in bio_user:
                if str(userinfo.username) == str(bio.username):
                    context['button'] = "Follow button off"
   
    if 'follow' in request.POST:
        user1 = User.objects.get(username=request.POST['follow'])
        user = User.objects.get(username=request.user)
        bio = Bio.objects.get(user=request.user)
        bio.following.add(user1)
        bio.save() 
        buttonchecker()
        context["message"] ="Following"
        if str(user1.username) !=str(request.user):
            context['loged_in_user'] ="goAhead"
        return render(request, 'grumblr/profile.html',context)

    if 'unfollow' in request.POST:
        user1 = User.objects.get(username=request.POST['unfollow'])
        user = User.objects.get(username=request.user)
        bio = Bio.objects.get(user=request.user)
        bio.following.remove(user1)
        bio.save()
        buttonchecker()
        context["message"] ="Unfollowed"
        if str(user1.username) != str(request.user):
            context['loged_in_user'] ="goAhead"
        return render(request, 'grumblr/profile.html',context)

    buttonchecker()
    if str(user.username) != str(request.user):
        context['loged_in_user'] ="goAhead"
    form1 = Comment(request.POST)
    context['form1'] = form1
    context['form1'] = Comment()

    return render(request, 'grumblr/profile.html',context)


#-----------Index page login(check if the password & username match)------------#
def index(request):
    errors =[]
    context={}
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        user = authenticate(username=request.user.username, password=user.password)
        login(request,user)
        return redirect('/globalpage/')

    if(request.method=='GET'):
        context['form'] = Index()
        return render(request, 'grumblr/index.html', context)
    form = Index(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render (request, 'grumblr/index.html', context)

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is not None:
        login(request,user)
        return redirect('/globalpage/')

#--------------------Edit page updation------------------------------------
@login_required
def editpage(request):
    username = request.user.id
    bio = Bio.objects.get(user=(username))
    documents = Document.objects.filter(user=username)
    context = {}

    if request.method =='GET':
        context = {'bio':bio, 'documents':documents}
        context['form'] = Editpage()
        context['form1'] = DocumentForm()
        return render(request,'grumblr/editpage.html',context)

    form = Editpage(request.POST)

    form1 = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        owner = User.objects.get(id=request.user.id)
        bio = Bio.objects.get(user=owner)
        if form.cleaned_data['first']:
            owner.first_name = form.cleaned_data['first']

        if form.cleaned_data['last']:
            owner.last_name = form.cleaned_data['last']
 
        if form.cleaned_data['age']:
            bio.age = form.cleaned_data['age']

        if form.cleaned_data['bio']:
            bio.short_bio = form.cleaned_data['bio']
        bio.save()
        owner.save()
        user = User.objects.get(id=request.user.id)
        documents = Document.objects.filter(user=request.user)
        if documents:
            documents = Document.objects.get(user=username)
        context={'bio': bio, 'user':user, 'documents': documents}
        context['form1'] = DocumentForm()
        context['form'] = Editpage()
        return render (request, 'grumblr/editpage.html', context)

    if form1.is_valid():
        documents = Document.objects.filter(user=request.user)
        if documents:
            documents = Document.objects.get(user=request.user)
            documents.docfile.delete(save=False)
            documents.docfile=request.FILES['docfile']
            documents.save()
        else:
            newdoc = Document(docfile = request.FILES['docfile'], user=request.user)
            newdoc.save()
        documents = Document.objects.get(user=request.user)
        bio = Bio.objects.filter(user=request.user)
        if bio:
            bio = Bio.objects.get(user=request.user)

        context = {'documents' : documents, 'bio':bio}
        context['form1'] = DocumentForm()
        context['form'] = Editpage()

        return render (request, 'grumblr/editpage.html', context)


    if not form1.is_valid():
        documents = Document.objects.filter(user=request.user)
        if documents:
            documents = Document.objects.get(user=request.user)
            bio = Bio.objects.filter(user=request.user)
            if bio:
                bio = Bio.objects.get(user=request.user)
                #bio = bio[0];
            context = {'documents' : documents, 'bio':bio}
            context['form1'] = form1
            context['form'] = form
            return render(request, 'grumblr/editpage.html', context)
        else:

            bio = Bio.objects.filter(user=request.user)
            
            if bio:
                bio = Bio.objects.get(user=request.user)
            context = {'bio':bio}
            context['form1'] = form1
            context['form'] = form
            return render(request, 'grumblr/editpage.html', context)

    if not form.is_valid():
        context['form'] = form
        context['form1'] = form1
        return render(request, 'grumblr/editpage.html', context)

#------------------------Password reset email-----------------------------------
def getemail(request): 
    context = {}
    if request.method=='GET':
        context['form'] = GetEmail()
        return render(request,'grumblr/emailpage.html',context)

    form = GetEmail(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render (request, 'grumblr/emailpage.html', context)

    emailAddress=request.POST['email1']
    username = request.POST['username1']
    user = User.objects.filter(username=request.POST['username1'])

    user = User.objects.get(username=request.POST['username1'])
    token = default_token_generator.make_token(user)
    Bio.objects.filter(user=user).update(token=token)
    email_body = """Please click on the link below to reset password
    http://%s%s"""%(request.get_host(), reverse('confirm', args=(username, token)))     
    send_mail(subject = "grumblr Change Password", message = email_body, from_email = "desaiparth1812@gmail.com", recipient_list =[user.email])
    message = []
    message.append("Change/Reset password link sent to your registered Email ID")
    context ={'message':message[0]}
    context['form']  = GetEmail();
    return render (request, 'grumblr/emailpage.html', context)

#-------------------Implements the follower logic-----------------------------
@login_required
def followerdisplay(request):
    context = {}
    bio_user = Bio.objects.get(user=request.user)
    allfollowers = bio_user.following.all()
    documents = Document.objects.all()
    items = Post.objects.all()
    allcomments = Comments.objects.all()
    context = {'bio':bio_user, 'items': items, 'documents':documents, 'allcomments':allcomments, 'allfollowers':allfollowers}
    image = Document.objects.filter(user=request.user)
    if image:
        image = Document.objects.get(user=request.user)
        context = {'bio':bio_user, 'items': items, 'documents':documents, 'allcomments':allcomments, 'allfollowers':allfollowers, 'image':image}
    form1 = Comment(request.POST)
    context['form1'] = form1
    context['form1'] = Comment()
    return render (request, 'grumblr/follower.html', context)


#-----------Leds to the chnage password page if token/username are correct and match----------
def changepassword(request, username, token):
    context ={}
    user = User.objects.filter(username=username)
    if not  user:
        return redirect('/index/')
    if user is not None:
        user = User.objects.get(username=username)
        bio = Bio.objects.get(user=user)
        token_database = bio.token
        if token_database != token:
            return redirect('/index/')
        context['username'] = user.username
        context['form2'] = ChangePassword()
        return render(request, 'grumblr/changepassword.html', context)

#------------------Confirms the link for new registered users---------------------
def emailconfirm(request, username, token):
    context ={}
    user = User.objects.filter(username=username)

    if not  user:
        return redirect('/index/')

    if user is not None:
        user = User.objects.get(username=username)
        bio = Bio.objects.get(user=user)
        token_database = bio.token
        if token_database != token:
            return redirect('/index/')
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/profile/')


#------------Implements the change in password --------------
def changepasswordimplementation(request):
    context = {}
    username = request.POST['changepassword']
    context['username'] = username

    if request.POST == 'GET':
        return redirect ('/profile/')

    form = ChangePassword(request.POST)
    context['form2'] = form

    if not form.is_valid():
        return render(request, 'grumblr/changepassword.html', context)

    username = request.POST['changepassword']
    owner = User.objects.get(username=username)
    owner.set_password(request.POST['password1'])
    owner.save()
    owner = User.objects.get(username=username)
    login(request, owner)
    return redirect('/globalpage/')

#---------------404-----------------
def wrongurl(request):
    return render(request, 'grumblr/error.html')


#---Handles the ajax request to update global page every 5 seconds and sends new post and comments if any---
@login_required
def globalpage_ajax(request):
    comments=[]
    pk = request.GET.get("data")
    if (pk is None): 
        pk = 0
    newPost = Post.objects.filter(id__gt=pk).reverse()
    if newPost:
        for i in newPost:
            comments += Comments.objects.filter(userpost=i)
        response = list(newPost) + list(User.objects.all()) + list(Document.objects.all()) + list(comments)
        responseText = serializers.serialize("json", response)
        return HttpResponse(responseText, content_type ="application/json")
    else:
        return HttpResponse("")


#----------------When you click on the username to see that persons profile ---------------------
@login_required
def prof(request, username):
    user = User.objects.get(username=username)
    userinfo =User.objects.get(username=user)
    posts=Post.objects.filter(user=userinfo)
    documents = Document.objects.all()
    image_user = Document.objects.filter(user=userinfo)
    allcomments = Comments.objects.all()

    bio = Bio.objects.get(user=userinfo)
    if documents:
        context ={'items':posts,'user':user, 'documents': documents, 'bio':bio, 'image_user':image_user,'allcomments':allcomments}
    else:
        context ={'items':posts,'user':user, 'bio':bio, 'image_user':image_user, 'allcomments':allcomments}

    def buttonchecker():
        bio_user = Bio.objects.get(user=request.user)
        if bio_user:
            bio_user = bio_user.following.all()
            for bio in bio_user:
                if str(userinfo.username) == str(bio.username):
                    context['button'] = "Follow button off"
    
    buttonchecker()
    if str(user.username) != str(request.user):
        context['loged_in_user'] ="goAhead"

    return render(request, 'grumblr/profile.html',context)


#-------Handles Ajax Request and Sends a HttpResponse with Json data-------#
@login_required
def comment(request, postid):
    context ={}
    form = Comment(request.POST)
    ItemObject = Post.objects.get(id=postid)
    user = request.user
    newcomm= request.POST['comment']
    form = Comment(newcomm)
    context['form'] = form 
    new_comment = Comments(user=request.user, userpost = ItemObject, usercomment=newcomm)
    new_comment.save()
    comment_send = Comments.objects.filter(usercomment=newcomm).filter(user=user).filter(userpost = ItemObject)
    user_send = User.objects.filter(username=request.user)
    images = Document.objects.filter(user=user)
    response = list(comment_send)+list(user_send) +list(images)
    responseText = serializers.serialize("json", response)
    return HttpResponse(responseText, content_type ="application/json")






    







