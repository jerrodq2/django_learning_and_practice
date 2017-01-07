from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    message = models.TextField(max_length=200)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class Post(models.Model):
    post = models.TextField(max_length=100)
    user_id = models.ForeignKey(User)
    message_id = models.ForeignKey(Message)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
