"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# @author Parth Desai
# parthd@andrew.cmu.edu

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

import grumblr.views 
urlpatterns =static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', grumblr.views.signup, name = 'signup'),
    url(r'^globalpage/', grumblr.views.globalpage, name = 'globalpage'),
    url(r'^globalpage_ajax/', grumblr.views.globalpage_ajax, name = 'globalpage_ajax'),
    url(r'^index/', grumblr.views.index, name ='index'),
    url(r'^logout/', auth_views.logout_then_login, name ='logout'),
    url(r'^signup/', grumblr.views.signup, name ='signup'),
    url(r'^profile/', grumblr.views.profile, name ='profile'),
    url(r'^editpage/', grumblr.views.editpage, name ='editpage'),
    url(r'^emailpage/', grumblr.views.getemail, name ='emailpage'),
    url(r'^followerdisplay/', grumblr.views.followerdisplay, name ='followerdisplay'),
    url(r'^confirm/(?P<username>[\w.@+-]+)/(?P<token>[\w.@+-]+)$', grumblr.views.changepassword, name="confirm"),
    url(r'^emailconfirm/(?P<username>[\w.@+-]+)/(?P<token>[\w.@+-]+)$', grumblr.views.emailconfirm, name="emailconfirm"),
    url(r'^prof/(?P<username>[\w.@+-]+)$', grumblr.views.prof, name="prof"),
    url(r'^changepassword/', grumblr.views.changepasswordimplementation,name = 'changepassword'),
    url (r'^comment/(\d+)', grumblr.views.comment, name= 'comment'),
    url(r'^$', grumblr.views.index, name ='index'),
    url(r'^', grumblr.views.wrongurl, name= 'wrongurl'),
] 

