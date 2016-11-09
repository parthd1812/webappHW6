
# @author Parth Desai
# parthd@andrew.cmu.edu

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from grumblr.validators import validate_file_extension

from datetime import datetime

import os
from django.core.exceptions import ValidationError



class Post(models.Model):
    text = models.CharField(max_length=42)
    date_time = models.DateTimeField(auto_now="True")
    user = models.ForeignKey(User)
    class Meta:
        ordering = ["-date_time"]

    def __unicode__(self):
        return '%s %s %s' % (self.text, self.date_time, self.user)

class Bio(models.Model):
    short_bio = models.CharField(max_length=420)
    age = models.IntegerField()
    token = models.CharField(max_length=40,default='')
    user = models.OneToOneField(User)
    #user = models.ForeignKey(User)
    following = models.ManyToManyField(User, symmetrical=False, related_name="follow+")


    def __unicode__(self):
        return '%s %d %s %s' % (self.short_bio, self.age, self.user, self.following) 

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', validators=[validate_file_extension])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    user = models.ForeignKey(User)
    userpost = models.ForeignKey(Post)
    usercomment = models.TextField(max_length=42)
    date_time = models.DateTimeField(auto_now="True")
    class Meta:
        ordering = ["date_time"]
