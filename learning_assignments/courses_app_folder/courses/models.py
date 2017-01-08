from __future__ import unicode_literals

from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30, default='desc')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=50)
    course = models.ForeignKey(Course, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
