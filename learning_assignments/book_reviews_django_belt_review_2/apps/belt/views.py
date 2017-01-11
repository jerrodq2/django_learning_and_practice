from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Author, Book, Review

def index(request):
    if 'id' in request.session:
        return redirect(reverse('belt:books'))
    return render(request, 'belt/index.html')

def register(request):
    if request.method != 'POST':
        return redirect(reverse('belt:index'))
    user = User.objects.register(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('belt:index'))
    request.session['id'] = user['id']
    request.session['name'] = user['name']
    return redirect(reverse('belt:books'))

def login(request):
    if request.method != 'POST':
        return redirect(reverse('belt:books'))
    user = User.objects.login(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('belt:books'))
    request.session['id'] = user['id']
    request.session['name'] = user['name']
    return redirect(reverse('belt:books'))

def logout(request):
    del request.session['id']
    del request.session['name']
    return redirect(reverse('belt:index'))

def books(request):
    if not 'id' in request.session:
        return redirect(reverse('belt:index'))
    three = Book.objects.three_most_recent()
    context = {
        'books': Book.objects.all(),
        'three': three
    }
    return render(request, 'belt/book.html', context)

def add(request):
    if not 'id' in request.session:
        return redirect(reverse('belt:index'))
    return render(request, 'belt/add.html', {'authors': Author.objects.all()} )

def add_review(request):
    if request.method != 'POST':
        return redirect(reverse('belt:add'))
    book = Book.objects.add_book(request.POST, request.session['id'])
    if book['errors']:
        for error in book['errors']:
            messages.info(request, error)
        return redirect(reverse('belt:add'))
    return redirect(reverse('belt:books'))

def show(request, id):
    if not 'id' in request.session:
        return redirect(reverse('belt:index'))
    book = Book.objects.get_book(id)
    context = {
        'book': book['book'],
        'reviews': book['reviews']
    }
    return render(request, 'belt/show.html', context)

def destroy(request, rid, bid):
    if not 'id' in request.session:
        return redirect(reverse('belt:index'))
    Book.objects.destroy_review(rid, request.session['id'])
    return redirect(reverse('belt:show', kwargs={'id': bid}))

def createReview(request, id):
    if request.method != 'POST':
        return redirect(reverse('belt:show', kwargs={'id': id}))
    review = Book.objects.create_review(request.POST, id, request.session['id'])
    if review['errors']:
        for error in review['errors']:
            messages.info(request, error)
    return redirect(reverse('belt:show', kwargs={'id': id}))

def user(request, id):
    if not 'id' in request.session:
        return redirect(reverse('belt:index'))
    user = User.objects.get_user(id)
    context = {
        'user': user['user'],
        'reviews': user['reviews'],
        'length': user['length']
    }
    return render(request, 'belt/user.html', context)
