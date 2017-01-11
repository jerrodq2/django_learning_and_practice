from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Author, Book, Review



def index(request):
    return render(request, 'belt/index.html')

def reg(request):
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
        return redirect(reverse('belt:index'))
    user = User.objects.login(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('belt:index'))
    request.session['id'] = user['id']
    request.session['name'] = user['name']
    return redirect(reverse('belt:books'))

def logout(self):
    del request.session['id']
    del request.session['name']
    return redirect(reverse('belt:index'))

def books(request):
    if 'id' not in request.session:
        return redirect(reverse('belt:index'))
    book = Book.objects.books()
    context = {
        'books': Book.objects.all(),
        'three': book,
        }
    return render(request, 'belt/books.html', context)

def add(request):
    if 'id' not in request.session:
        return redirect(reverse('belt:index'))
    authors = Author.objects.all()
    return render(request, 'belt/add.html', {'authors': authors})

def create(request):
    if 'id' not in request.session:
        return redirect(reverse('belt:index'))
    if request.method != 'POST':
        return redirect(reverse('belt:index'))
    book = Book.objects.new(request.POST)
    if book['errors']:
        for i in book['errors']:
            messages.info(request, i)
        return redirect(reverse('belt:add'))
    return redirect(reverse('belt:books'))

def review(request, id):
    book = Book.objects.review(request.POST, id)
    if book['errors']:
        for i in book['errors']:
            messages.info(request, i)
    return redirect(reverse('belt:show', kwargs={'id':id}))

def destroy(request):
    pass

def show(request, id):
    if 'id' not in request.session:
        return redirect(reverse('belt:index'))
    data = Book.objects.showBook(id)
    return render(request, 'belt/show.html', {'book':data['book'], 'ratings':data['ratings']} )

def user(request):
    pass
