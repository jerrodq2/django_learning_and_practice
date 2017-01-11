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
            errors.append('Name cannot be empty')
        elif len(data['name']) < 4:
            errors.append('Name must be at least 4 characters long')
        if len(data['alias']) == 0:
            errors.append('Alias cannot be empty')
        elif len(data['alias']) < 4:
            errors.append('Alias must be at least 4 characters long')
        if len(data['email']) == 0:
            errors.append('Email cannot be empty')
        elif not reg.match(data['email']):
            errors.append('Invalid Email')
        if len(data['password']) == 0:
            errors.append('Password cannot be empty')
        elif len(data['password']) < 4:
            errors.append('Password must be at least 4 characters long')
        elif data['password'] != data['confirm']:
            errors.append('Confirmation password must match Password')
        if errors:
            return {'errors': errors}
        user = User.objects.filter(email=data['email'])
        if len(user) != 0:
            return {'errors': ['Email already in use']}
        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        try:
            user = User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password=password)
        except:
            return {'errors': ['There was an error']}
        return {'errors': errors, 'id': user.id, 'name':user.name}

    def login(sefl, data):
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
        password= bcrypt.hashpw(data['password'].encode(), user.password.encode())
        if user.password != password:
            return {'errors': ['Wrong Password']}
        return  {'errors': errors, 'id': user.id, 'name':user.name}

    def get_user(self, id):
        user = User.objects.get(pk=id)
        reviews = Review.objects.filter(user=user)
        length = len(reviews)
        return {'user': user, 'reviews': reviews, 'length': length}





class BookManager(models.Manager):
    def three_most_recent(self):
        three = Book.objects.all().order_by('-id')[:3]
        for i in three:
            rating = Review.objects.filter(book=i).aggregate(Avg('rating'))
            rating = math.floor( round(rating['rating__avg'], 0) )
            rating = int(rating)
            arr = []
            left = []
            for x in range(0, rating):
                arr.append(0)
            for x in range(rating, 5):
                left.append(0)
            i.rating = arr
            i.left = left
            i.review = Review.objects.filter(book=i)[0]
        return three
    def add_book(self, data, id):
        errors = []
        if len(data['title']) == 0:
            errors.append('Title cannot be empty')
        elif len(data['title']) < 4:
            errors.append('Title must be at least 4 characters long')
        if len(data['review']) == 0:
            errors.append('Review cannot be empty')
        elif len(data['review']) < 4:
            errors.append('Review must be at least 4 characters long')
        if len(data['author']) == 0 and len(data['new_author']) == 0:
            errors.append('Old or new author must be entered')
        if len(data['rating']) == 0:
            errors.append('Rating cannot be empty')
        if errors:
            return {'errors': errors}

        if len(data['new_author']) != 0:
            author = Author.objects.create(name=data['new_author'])
        else:
            author = Author.objects.get(name=data['author'])

        user = User.objects.get(pk=id)
        try:
            book = Book.objects.create(title=data['title'], author = author)
        except:
            return {'errors': ['There was ane rror']}
        Review.objects.create(book=book, user=user, rating=data['rating'], review=data['review'])
        return {'errors': errors}

    def get_book(self, id):
        book = Book.objects.get(pk=id)
        reviews = Review.objects.filter(book=book)
        for i in reviews:
            i.rating = int(i.rating)
            arr = []
            left = []
            for x in range(0, i.rating):
                arr.append(0)
            for x in range(i.rating, 5):
                left.append(0)
            i.rating = arr
            i.left = left
        return {'book': book, 'reviews': reviews}

    def destroy_review(self, id, uid):
        try:
            review = Review.objects.get(pk=id)
        except:
            return
        user = User.objects.get(pk=uid)
        if user != review.user:
            return
        review.delete()
        return

    def create_review(self, data, id, uid):
        errors = []
        if len(data['review']) == 0:
            errors.append('Review cannot be emtpy')
        if len(data['rating']) == 0:
            errors.append('Rating cannot be emtpy')
        if len(data['review']) < 4:
            errors.append('Review must be at least 4 characters long')
        if errors:
            return {'errors': errors}

        user = User.objects.get(pk=uid)
        book = Book.objects.get(pk=id)
        Review.objects.create(user=user, book=book, review=data['review'], rating=data['rating'])
        return {'errors': errors}







class User(models.Model):
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    review = models.CharField(max_length=100)
    rating = models.FloatField()
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
