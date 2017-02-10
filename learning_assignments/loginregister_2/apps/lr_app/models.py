from __future__ import unicode_literals

from django.db import models

import re, bcrypt
reg = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class UserManager(models.Manager):
    def register(self, data):
        errors = []
        if not data.has_key('first_name'):
            errors.append('First name cannot be blank')
        elif len(data['first_name']) == 0:
            errors.append('First name cannot be blank')
        elif len(data['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        if not data.has_key('last_name'):
            errors.append('Last name cannot be blank')
        elif len(data['last_name']) == 0:
            errors.append('Last name cannot be blank')
        elif len(data['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        if not data.has_key('email'):
            errors.append('Email name cannot be blank')
        elif len(data['email']) == 0:
            errors.append('Email is required')
        elif not reg.match(data['email']):
            errors.append('Email is in invalid format')
        if not data.has_key('password'):
            errors.append('Password name cannot be blank')
        elif not data.has_key('confirmation'):
            errors.append('Confirmation password cannot be blank')
        elif len(data['password']) == 0:
            errors.append('Password is required')
        elif len(data['password']) < 4:
            errors.append('Password must be at least 4 characters long')
        elif data['password'] != data['confirmation']:
            errors.append('Password and confirmation password must match')
        if errors:
            return {'errors': errors}

        currentUser = User.objects.filter(email=data['email'])
        if len(currentUser) != 0:
            return {'errors': ['Email already in use']}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=password)
        return {'errors': errors, 'name':data['first_name']}

    def login(self, data):
        errors = []
        if not data.has_key('email'):
            errors.append('Email name cannot be blank')
        elif len(data['email']) == 0:
            errors.append('Email is required')
        if not data.has_key('password'):
            errors.append('Password name cannot be blank')
        elif len(data['password']) == 0:
            errors.append('Password is required')
        if errors:
            return {'errors': errors}

        try:
            user = User.objects.get(email = data['email'])
        except:
            return {'errors': ['Email not found']}
        password = bcrypt.hashpw(data['password'].encode(), user.password.encode())
        if user.password != password:
            return {'errors': ['Wrong password']}
        return {'errors': errors, 'name': user.first_name}




class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
