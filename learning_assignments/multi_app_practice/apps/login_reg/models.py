from __future__ import unicode_literals

from django.db import models
import re, bcrypt
reg = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class UserManager(models.Manager):
    def reg(self, data):
        errors = []
        if len(data['first']) == 0:
            errors.append('First Name is required')
        elif len(data['first']) < 2:
            errors.append('First Name must be at least 2 characters long')
        if len(data['last']) == 0:
            errors.append('Last Name is required')
        elif len(data['last']) < 2:
            errors.append('Last Name must be at least 2 characters long')
        if len(data['email']) == 0:
            errors.append('Email is required')
        elif not reg.match(data['email']):
            errors.append('Email is in invalid format')
        if len(data['password']) == 0:
            errors.append('Password is required')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif data['password'] != data['conf']:
            errors.append('Password and Confirmation password must match')
        if errors:
            return {'errors': errors}
        #lets make sure the email doesn't already exist in the db
        user = User.UserManager.filter(email=data['email'])
        if len(user) != 0:
            return {'errors': ['Email is already in the database']}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        User.UserManager.create(first_name=data['first'], last_name=data['last'], email=data['email'], password=password)
        user = User.UserManager.filter(email=data['email'])
        return {'errors': errors, 'name':data['first'], 'id': user[0].id}

    def login(self, data):
        errors = []
        if len(data['log_email']) == 0:
            errors.append('Email is required')
        if len(data['log_password']) == 0:
            errors.append('Password is required')
        if errors:
            return {'errors': errors}
        user = User.UserManager.filter(email = data['log_email'])
        if len(user) == 0:
            errors.append('Email not found')
            return {'errors': errors}
        log_password= bcrypt.hashpw(data['log_password'].encode(), user[0].password.encode())
        if log_password == user[0].password:
            return {'errors': errors, 'name': user[0].first_name, 'id': user[0].id}
        errors.append('Invalid Password')
        return {'errors': errors}




class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    UserManager = UserManager()
