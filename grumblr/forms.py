
# @author Parth Desai
# parthd@andrew.cmu.edu

from django import forms
from django.contrib.auth.models import User
from grumblr.validators import validate_file_extension
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError

class Index(forms.Form):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Username'}))
    password = forms.CharField(max_length = 30, widget=forms.PasswordInput(attrs={'class': 'box', 'placeholder':'Password'}))

    def clean(self):
        cleaned_data = super(Index,self).clean()
        user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('Invalid Username and Password')

        return cleaned_data

class Signup(forms.Form):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Username'}))
    first = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'First Name'}))
    last = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length = 30, widget=forms.PasswordInput(attrs={'class': 'box', 'placeholder':'Password'}))
    password2 = forms.CharField(max_length = 30, widget=forms.PasswordInput(attrs={'class': 'box', 'placeholder':'Password'}))

    def clean(self):
        cleaned_data = super(Signup, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1!= password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username):
            raise forms.ValidationError("Username is already taken.")

class Globalpage(forms.Form):
    post = forms.CharField(max_length = 42, widget=forms.TextInput(attrs={'class': 'textbox form-control', 'placeholder': 'Add your post here'}))
    

    def clean(self):
        cleaned_data = super(Globalpage,self).clean()
        return cleaned_data

class Editpage(forms.Form):
    age=forms.IntegerField(max_value=150, min_value = 0)
    first = forms.CharField(required=False,  max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Change your First Name'}))
    last = forms.CharField(required=False,  max_length = 30, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Change your Last Name'}))
    bio  = forms.CharField(required=False,  max_length = 420, widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Add you bio'}))

    

    def clean(self):
        cleaned_data = super(Editpage,self).clean()
        return cleaned_data

class DocumentForm(forms.Form): 
    docfile = forms.FileField (label = 'Select a file', validators=[validate_file_extension])

    def clean(self):
        cleaned_data = super(DocumentForm,self).clean()
        return cleaned_data

class ChangePassword(forms.Form):
    password1 = forms.CharField(max_length = 30, widget=forms.PasswordInput(attrs={'class': 'box', 'placeholder':'Password'}))
    password2 = forms.CharField(max_length = 30, widget=forms.PasswordInput(attrs={'class': 'box', 'placeholder':'Confirm Password'}))
    
    def clean(self):
        cleaned_data = super(ChangePassword, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1!= password2:
            print "jnfjnvfnvjnfjvfvjvnfjvj"
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class GetEmail(forms.Form):
    username1 = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box','placeholder': 'Username'}))
    email1 = forms.EmailField(max_length = 30, widget=forms.TextInput(attrs={'class': 'box','placeholder': 'Email'}))
    
    def clean(self):
        cleaned_data = super(GetEmail, self).clean()
        username11 = cleaned_data.get('username1')
        print username11
        email11 = cleaned_data.get('email1')
        print email11
        user = User.objects.filter(username=username11)
        if not user:
            raise forms.ValidationError("No account with given username ")
        
        user1 = User.objects.filter(username=username11)
        if user1:
            user1 = user1[0]
            if not (username11 == user1.username and email11 == user1.email):
                print "correct"
                raise forms.ValidationError("Given Username and Email do not match")
        return cleaned_data

class Comment (forms.Form):
    comment = forms.CharField(required=True, max_length = 42, widget=forms.TextInput(attrs={'placeholder': 'Add your comment here'}))
    hiddenpk = forms.IntegerField(widget = forms.HiddenInput)

    def clean(self):
        cleaned_data = super(Comment,self).clean()
        return cleaned_data


            






