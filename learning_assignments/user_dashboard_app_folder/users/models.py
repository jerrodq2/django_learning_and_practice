from __future__ import unicode_literals
from django.db import models
import re, bcrypt
reg = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')


class UserManager(models.Manager):
    def register(self, data):
        errors = []
        if len(data['email']) == 0:
            errors.append('Email cannot be empty')
        elif not reg.match(data['email']):
            errors.append('Invalid email format')
        if len(data['first_name']) == 0:
            errors.append('First Name cannot be empty')
        if len(data['last_name']) == 0:
            errors.append('Last Name cannot be empty')
        if len(data['password']) == 0:
            errors.append('Password cannot be empty')
        if len(data['confirmation']) == 0:
            errors.append('Confirmation Password cannot be empty')
        elif data['password'] != data['confirmation']:
            errors.append('Password must match confirmation password')
        if errors:
            return {'errors': errors}
        user = User.objects.filter(email=data['email'])
        if len(user) != 0:
            return {'errors': ['Email already in use']}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = User.objects.all()[:]
        if len(user) == 0:
            admin = True
        else:
            admin = False
        try:
            user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password = password, admin = admin)
        except:
            return {'errors': ['there was an error']}
        return {'errors': errors, 'id': user.id, 'admin': user.admin}



    def login(self, data):
        errors = []
        if len(data['email']) == 0:
            errors.append('Email cannot be empty')
        if len(data['password']) == 0:
            errors.append('Password cannot be empty')
        if errors:
            return {'errors': errors}
        try:
            user = User.objects.get(email=data['email'])
        except:
            return {'errors': ['Email not found']}
        password = bcrypt.hashpw(data['password'].encode(), user.password.encode())
        if password != user.password:
            return {'errors': ['Incorrect Password']}
        return {'errors': errors, 'id': user.id, 'admin': user.admin}


    def edit_main_info(self, data, id):
        errors = []
        if len(data['email']) == 0:
            errors.append('Email cannot be empty')
        elif not reg.match(data['email']):
            errors.append('Invalid email format')
        if len(data['first_name']) == 0:
            errors.append('First Name cannot be empty')
        if len(data['last_name']) == 0:
            errors.append('Last Name cannot be empty')
        if errors:
            return {'errors': errors}
        user = User.objects.filter(email=data['email']).exclude(pk=id)
        if len(user) != 0:
            return {'errors': ['Email already in use']}
        user = User.objects.get(pk=id)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        try:
            user.save()
        except:
            return {'errors': ['There was an error']}
        return {'errors': errors}

    def edit_description(self, data, id):
        if len(data['description']) == 0:
            return {'errors': ['Description cannot be empty']}
        user = User.objects.get(pk=id)
        user.description = data['description']
        user.save()
        return {'errors': []}

    def edit_password(self, data, id):
        errors = []
        if len(data['password']) == 0:
            errors.append('Password cannot be empty')
        elif data['password'] != data['confirmation']:
            errors.append('Password must match confirmation password')
        if errors:
            return {'errors': errors}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = User.objects.get(pk=id)
        user.password = password
        user.save()
        return {'errors': errors}



    def admin_main_info(self, data, id):
        errors = []
        if len(data['email']) == 0:
            errors.append('Email cannot be empty')
        elif not reg.match(data['email']):
            errors.append('Invalid email format')
        if len(data['first_name']) == 0:
            errors.append('First Name cannot be empty')
        if len(data['last_name']) == 0:
            errors.append('Last Name cannot be empty')
        if errors:
            return {'errors': errors}
        user = User.objects.filter(email=data['email']).exclude(pk=id)
        if len(user) != 0:
            return {'errors': ['Email already in use']}
        if data['admin'] == 'Normal':
            admin = False
        else:
            admin = True
        user = User.objects.get(pk=id)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.admin = admin
        try:
            user.save()
        except:
            return {'errors': ['There was an error']}
        return {'errors': errors}


    def admin_edit_password(self, data, id):
        errors = []
        if len(data['password']) == 0:
            errors.append('Password cannot be empty')
        elif data['password'] != data['confirmation']:
            errors.append('Password must match confirmation password')
        if errors:
            return {'errors': errors}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        user = User.objects.get(pk=id)
        user.password = password
        user.save()
        return {'errors': errors}

    def show(self, id):
        user = User.objects.values('email', 'description', 'created_at', 'id', 'first_name', 'last_name').get(pk=id)
        messages = Message.objects.filter(user=user['id'])
        for i in messages:
            comment = Comment.objects.filter(message = i)
            i.comments = comment
        return {'user': user, 'messages': messages}
#END OF USERMANAGER*******************************************************



class MessageManager(models.Manager):
    def new(self, data, id, cid):
        if len(data['message']) == 0:
            return {'errors': ['Message cannot be empty']}
        user = User.objects.get(pk=id)
        creator = User.objects.get(pk=cid)
        Message.objects.create(message=data['message'], user=user, creator=creator)
        return {'errors': []}

    def new_comment(self, data, id, cid, mid):
        if len(data['comment']) == 0:
            return {'errors': ['Comment cannot be empty']}
        user = User.objects.get(pk=id)
        creator = User.objects.get(pk=cid)
        message = Message.objects.get(pk=mid)
        Comment.objects.create(comment=data['comment'], user=user, creator=creator, message=message)
        return {'errors': []}











class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    admin = models.BooleanField(default=False)
    email = models.EmailField(max_length = 50)
    description = models.TextField(max_length=500, default=False)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length=200)
    user = models.ForeignKey(User, related_name='m_user')
    creator = models.ForeignKey(User, related_name='m_creator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    comment = models.TextField(max_length=200)
    user = models.ForeignKey(User, related_name='c_user')
    creator = models.ForeignKey(User, related_name='c_creator')
    message = models.ForeignKey(Message)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
