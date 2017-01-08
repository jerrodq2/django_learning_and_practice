from __future__ import unicode_literals

from django.db import models
import re
reg = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class CheckEmail(models.Manager):
    def checkEmail(self, data):
        errors = []
        if len(data) == 0:
            errors.append("Email is required")
        elif not reg.match(data):
            errors.append("Email is invalid")
        return {'errors': errors}
    def new(self, data):
        print '*****8888888888888'
        print data
        return Email.CheckEmail.create(email=data)
    def destroy(self, id):
        return Email.CheckEmail.get(pk=id).delete()


class Email(models.Model):
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CheckEmail = CheckEmail()
