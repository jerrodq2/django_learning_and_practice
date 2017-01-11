from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg
import math
import re, bcrypt
reg = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class UserManager(models.Manager):
    def register(self, data):
        errors = []
        if len(data['name']) == 0:
            errors.append('Name cannot be blank')
        if len(data['alias']) == 0:
            errors.append('Alias cannot be blank')
        if len(data['email']) == 0:
            errors.append('Email cannot be blank')
        elif not reg.match(data['email']):
            errors.append('Invalid Email')
        if len(data['password']) == 0:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 4:
            errors.append('Password must be at least 4 characters long')
        elif data['password'] != data['confirmation']:
            errors.append('Password doesnt match confirmation password')
        if errors:
            return {'errors': errors}
        user = User.objects.filter(email=data['email'])
        if len(user) != 0:
            return {'errors': ['Email already in use']}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        try:
            User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password='password')
        except:
            return {'errors': ['there was an error']}
        user = User.objects.get(email=data['email'])
        return {'errors': errors, 'name':user.alias, 'id':user.id}

    def login(self, data):
        errors = []
        if len(data['email']) == 0:
            errors.append('Email cannot be blank')
        if len(data['password']) == 0:
            errors.append('Password cannot be blank')
        if errors:
            return {'errors': errors}
        try:
            user = User.objects.get(email=data['email'])
        except:
            return {'errors': ['Email not found']}
        password = bcrypt.hashpw(data['password'].encode(), user.password.encode())
        if password != user.password:
            return {'errors': ['Incorrect Password']}
        return {'errors': errors, 'name':user.alias, 'id':user.id}


class BookManager(models.Manager):
    def new(self, data):
        errors = []
        if len(data['name']) == 0:
            errors.append('Name cannot be blank')
        if len(data['review']) == 0:
            errors.append('Review cannot be blank')
        if len(data['rating']) == 0:
            errors.append('Rating cannot be blank')
        if len(data['author']) == 0 and len(data['new_author']) == 0:
            errors.append('Old or new author must be entered')
        if errors:
            return {'errors': errors}
        if len(data['new_author']) != 0:
            author = Author.objects.create(name=data['new_author'])

        else:
            author = Author.objects.get(name=data['author'])
        try:
            book = Book.objects.create(title=data['name'], author=author)
        except:
            return {'errors': ['There was an error']}
        Review.objects.create(review=data['review'], rating=data['rating'], book = book)
        return {'errors': errors}

    def books(self):
        three = Book.objects.all().order_by('-id')[:3]
        threeRating = []
        for i in three:
            i.rating = Review.objects.filter(book=i).aggregate(Avg('rating'))
            i.rating = math.floor(round(i.rating['rating__avg'], 0))
            i.rating = int(i.rating)
            arr = []
            left = []
            for x in range(0, i.rating):
                arr.append(0)
            for x in range(i.rating, 5):
                left.append(0)
            i.left = left
            i.rating = arr
            i.review = Review.objects.filter(book=i)[0]
            i.review = i.review.review
        return three

    def showBook(self, id):
        book = Book.objects.filter(pk=id)
        ratings = Review.objects.filter(book = book[0])
        for i in ratings:
            i.rating = int(i.rating)
            arr = []
            left = []
            for x in range(0,i.rating):
                arr.append(0)
            for x in range(i.rating, 5):
                left.append(0)
            i.rating = arr
            i.left = left

        return {'book':book[0], 'ratings':ratings}
    def review(self, data, id):
        errors = []
        if len(data['review']) == 0:
            errors.append('Review cannot be blank')
        if len(data['rating']) == 0:
            errors.append('Rating must be selected')
        if errors:
            return {'errors': errors}
        book = Book.objects.get(pk=id)
        Review.objects.create(review=data['review'], rating=data['rating'], book=book)
        return {'errors': errors}






class User(models.Model):
    name = models.CharField(max_length =50)
    alias = models.CharField(max_length =50)
    email = models.CharField(max_length =50)
    password = models.CharField(max_length =100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    review = models.CharField(max_length=100)
    rating = models.FloatField()
    book = models.ForeignKey(Book, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
