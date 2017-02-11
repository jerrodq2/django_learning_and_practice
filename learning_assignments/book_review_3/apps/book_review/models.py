from __future__ import unicode_literals
from django.db.models import Avg
from django.db import models
import math
import re, bcrypt
reg = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class UserManager(models.Manager):
    def login(self, data):
        errors = []
        if not data.has_key('email'):
            errors.append('Email is required')
        elif len(data['email']) == 0:
            errors.append('Email cannot be blank')
        if not data.has_key('password'):
            errors.append('Password is required')
        elif len(data['password']) == 0:
            errors.append('Password cannot be blank')
        if errors:
            return {'errors': errors}

        try:
            user = User.objects.get(email=data['email'])
        except:
            return {'errors': ['Email not found']}

        password = bcrypt.hashpw(data['password'].encode(), user.password.encode())
        if user.password != password:
            return {'errors': ['Invalid password']}
        return {'errors': errors, 'id': user.id, 'name': user.name}

    def register(self, data):
        errors = []
        if not data.has_key('name'):
            errors.append('Name is required')
        elif len(data['name']) == 0:
            errors.append('Name cannot be blank')
        elif len(data['name']) < 4:
            errors.append('Name must be at least 4 characters long')
        if not data.has_key('alias'):
            errors.append('Alias is required')
        elif len(data['alias']) == 0:
            errors.append('Alias cannot be blank')
        elif len(data['alias']) < 4:
            errors.append('Alias must be at least 4 characters long')
        if not data.has_key('email'):
            errors.append('Email is required')
        elif len(data['email']) == 0:
            errors.append('Email cannot be blank')
        elif not reg.match(data['email']):
            errors.append('Invalid Email')
        if not data.has_key('password'):
            errors.append('Password is required')
        elif not data.has_key('confirm'):
            errors.append('Confirmation Password is required')
        elif len(data['password']) == 0:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 4:
            errors.append('Password must be at least 4 characters long')
        elif data['password'] != data['confirm']:
            errors.append('Confirmation password does not match password')
        if errors:
            return {'errors': errors}

        user = User.objects.filter(email = data['email'])
        if len(user) != 0:
            return {'errors': ['email already in use']}

        password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        try:
            user = User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], password=password)
        except:
            return {'errors': ['There was an error']}
        return {'errors': errors, 'id': user.id, 'name': user.name}

    def show(self, id):
        try:
            user = User.objects.get(pk=id)
        except:
            return {'error': ['User not found']}
        reviews = Review.objects.filter(user=user)
        length = len(reviews)
        return {'error': [], 'user': user, 'reviews': reviews, 'length':length}



class BookManager(models.Manager):
    def get_books(self):
        three_most_recent = Book.objects.all().order_by('-id')[:3]
        for i in three_most_recent:
            # the aggregate below gets all the reviews with that book, and groups them together by averaging the rating column
            rating = Review.objects.filter(book=i).aggregate(Avg('rating'))
            rating = math.floor( round(rating['rating__avg'], 0) )
            rating = int(rating)
            rate = []
            uncolored_star = []
            for x in range(0, rating):
                rate.append(0)
            for x in range(rating, 5):
                uncolored_star.append(0)
            i.rating = rate
            i.uncolored_star = uncolored_star
            i.review = Review.objects.filter(book=i)[0]
        return three_most_recent


    def create_book(self, data, id):
        errors = []
        if not data.has_key('title'):
            errors.append('Book title is required')
        elif len(data['title']) == 0:
            errors.append('Book title cannot be emtpy')
        if not data.has_key('author') or not data.has_key('new_author'):
            errors.append('Author or New Author is reqired')
        elif len(data['author']) == 0 and len(data['new_author']) == 0:
            errors.append('Must select an author or create a new author')
        if not data.has_key('review'):
            errors.append('Review is required')
        elif len(data['review']) == 0:
            errors.append('Review cannot be empty')
        if not data.has_key('rating'):
            errors.append('Rating is required')
        elif len(data['rating']) == 0:
            errors.append('Rating cannot be empty')
        if errors:
            return {'errors': errors}

        if len(data['new_author']) != 0:
            test = Author.objects.filter(name=data['new_author'])
            if len(test) != 0:
                author = Author.objects.get(name=data['new_author'])
            else:
                author = Author.objects.create(name=data['new_author'])
        else:
            try:
                author = Author.objects.get(name=data['author'])
            except:
                return {'errors': ['Author not found']}

        test = Book.objects.filter(title=data['title'])
        if len(test) != 0:
            return {'errors': ['Book already in system']}

        try:
            book = Book.objects.create(title=data['title'], author = author)
        except:
            return {'errors': ['There was an problem creating the book']}
        user = User.objects.get(pk=id)
        try:
            Review.objects.create(book=book, user=user, rating=data['rating'], review=data['review'])
        except:
            return {'errors': ['There was a problem creating the review']}
        return {'errors': []}


    def show_book(self, id):
        try:
            book = Book.objects.get(pk=id)
        except:
            return {'errors': ['Book not found']}
        reviews = Review.objects.filter(book=book)
        for i in reviews:
            rating = int(i.rating)
            colored_stars = []
            uncolored_stars = []
            for x in range(0, rating):
                colored_stars.append(0)
            for x in range(rating, 5):
                uncolored_stars.append(0)
            i.rating = colored_stars
            i.uncolored_stars = uncolored_stars
        return {'errors': [], 'book': book, 'reviews': reviews}





class ReviewManager(models.Manager):
    def create_review(self, data, book_id, user_id):
        errors = []
        if not data.has_key('review'):
            errors.append('Review is required')
        elif len(data['review']) == 0:
            errors.append('Review cannot be empty')
        if not data.has_key('rating'):
            errors.append('Rating is required')
        elif len(data['rating']) == 0:
            errors.append('Rating cannot be empty')
        if errors:
            return {'errors': errors}

        try:
            book = Book.objects.get(pk=book_id)
        except:
            return {'errors': ['Book not found']}
        user = User.objects.get(pk=user_id)
        try:
            Review.objects.create(book=book, user=user, rating=data['rating'], review=data['review'])
        except:
            return {'errors': ['There was a problem creating the review']}
        return {'errors': errors}

    def destroy_review(self, review_id, user_id):
        user = User.objects.get(pk=user_id)
        try:
            review = Review.objects.get(pk=review_id)
        except:
            return False
        if user != review.user:
            return False
        review.delete()
        return True








class User(models.Model):
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    # The related name is so I can access info in reverse or reverse loop ups. For exaple, if I had a book (the shining), to access its author, I could just query the book and type book.author.name But in reverse, to see a book attached to an author (the many in the one to many relationship), I could do this. author1 = some_author.books.all() since I have the books related_name to be 'books'. Now I could loop through the books as so, for book in author1.books.all

class Review(models.Model):
    review = models.CharField(max_length=100)
    rating = models.FloatField()
    book = models.ForeignKey(Book, related_name='book_reviews')
    user = models.ForeignKey(User, related_name='user_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
