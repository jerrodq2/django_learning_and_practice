from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Book, Author, Review

def check_id(request):
    if not 'id' in request.session:
        return redirect(reverse('br:index'))

def check_method(request):
    if request.method != 'Post':
        return redirect(reverse('br:index'))
def flash_messages(request, errors):
    for error in errors:
        messages.info(request, error)



    #********************** START OF USER ROUTES **************************

    # url(r'^$', views.index, name='index'),
def index(request):
    if 'id' in request.session:
        return redirect(reverse('br:books'))
    return render(request, 'book_review/index.html')

    # url(r'^login$', views.login, name='login'),
def login(request):
    check_method(request)
    user = User.objects.login(request.POST)
    if user['errors']:
        flash_messages(request, user['errors'])
        return redirect(reverse('br:index'))
    request.session['id'] = user['id']
    request.session['name'] = user['name']
    return redirect(reverse('br:books'))

    # url(r'^register$', views.register, name='register'),
def register(request):
    check_method(request)
    user = User.objects.register(request.POST)
    if user['errors']:
        flash_messages(request, user['errors'])
        return redirect(reverse('br:index'))
    request.session['id'] = user['id']
    request.session['name'] = user['name']
    return redirect(reverse('br:books'))

    # url(r'^logout$', views.logout, name='logout'),
def logout(request):
    del request.session['id']
    del request.session['name']
    return redirect(reverse('br:index'))

    # url(r'^user/(?P<id>\d+)$', views.show_user, name='show_user'),
def show_user(request, id):
    check_id(request)
    user = User.objects.show(id)
    if user['error']:
        flash_messages(request, user['error'])
        return redirect(reverse('br:index'))
    context = {
        'user': user['user'],
        'reviews': user['reviews'],
        'number_of_reviews': user['length']
    }
    return render(request, 'book_review/show_user.html', context)

    #********************** END OF USER ROUTES **************************



    #********************** START OF BOOK ROUTES **************************

    # url(r'^books$', views.books, name='books'),
def books(request):
    check_id(request)
    three_most_recent = Book.objects.get_books()
    context = {
        'three_most_recent': three_most_recent,
        'all_books': Book.objects.all()
    }
    return render(request, 'book_review/books.html', context)

    # url(r'^books/add$', views.add_book, name='add_book'),
def add_book(request):
    check_id(request)
    return render(request, 'book_review/add.html', {
    'authors': Author.objects.all()})

    # url(r'^books/create$', views.create_book, name='create_book'),
def create_book(request):
    check_method(request)
    check_id(request)
    book = Book.objects.create_book(request.POST, request.session['id'])
    if book['errors']:
        flash_messages(request, book['errors'])
    else:
        messages.info(request, 'Book and review successfully added')
    return redirect(reverse('br:add_book'))

    # url(r'^book/(?P<id>\d+)$', views.show_book, name='show_book'),
def show_book(request, id):
    check_id(request)
    book = Book.objects.show_book(id)
    if book['errors']:
        flash_messages(request, book['errors'])
        return redirect(reverse('br:books'))
    context = {
        'book': book['book'],
        'reviews': book['reviews']
    }
    return render(request, 'book_review/show_book.html', context)

    # url(r'^author/(?P<id>\d+)$', views.author, name='author'),
def author(request, id):
    context = {
        'author': Author.objects.get(pk=id),
        'books': Author.objects.get(pk=id).books.all()
    }
    return render(request, 'book_review/author.html', context)


    # url(r'^books/(?P<id>\d+)/reviews/create$', views.create_review, name='create_review'),
def create_review(request, id):
    check_id(request)
    check_method(request)
    review = Review.objects.create_review(request.POST, id, request.session['id'])
    if review['errors']:
        flash_messages(request, review['errors'])
    else:
        messages.info(request, 'Review successfully created')
    return redirect(reverse('br:show_book', kwargs={'id': id}))


    # url(r'^reviews/(?P<id>\d+)/destroy$', views.destroy_review, name='destroy_review'),
def destroy_review(request, book_id, review_id):
    check_id(request)
    destroy = Review.objects.destroy_review(review_id, request.session['id'])
    if not destroy:
        return redirect(reverse('br:index'))
    return redirect(reverse('br:show_book', kwargs={'id': book_id}))
