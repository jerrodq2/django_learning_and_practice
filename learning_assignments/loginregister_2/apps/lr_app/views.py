from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'lr_app/index.html')

def register(request):
    if request.method != 'POST':
        return redirect(reverse('lr:index'))
    user = User.objects.register(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('lr:index'))
    messages.success(request, user['name'])
    return redirect(reverse('lr:success'))

def login(request):
    if request.method != 'POST':
        return redirect(reverse('lr:index'))
    user = User.objects.login(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('lr:index'))
    messages.success(request, user['name'])
    return redirect(reverse('lr:success'))

def success(request):
    return render(request, 'lr_app/success.html')
