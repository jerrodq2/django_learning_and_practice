from django.shortcuts import render, redirect
from ..users.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages


def index(request):
    return render(request, 'login_reg/index.html')

def signin(request):
    return render(request, 'login_reg/login.html')

def register(request):
    return render(request, 'login_reg/register.html')

def register_create(request):
    if request.method != 'POST':
        return redirect(reverse('login_reg:index'))
    user = User.objects.register(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('login_reg:register'))
    request.session['id'] = user['id']
    request.session['admin'] = user['admin']
    if(request.session['admin']):
        return redirect(reverse('users:admin'))
    else:
        return redirect(reverse('users:index'))

def login(request):
    if request.method != 'POST':
        return redirect(reverse('login_reg:index'))
    user = User.objects.login(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('login_reg:signin'))
    request.session['id'] = user['id']
    request.session['admin'] = user['admin']
    if(request.session['admin']):
        return redirect(reverse('users:admin'))
    else:
        return redirect(reverse('users:index'))

def logout(request):
    del request.session['id']
    del request.session['admin']
    return redirect(reverse('login_reg:index'))
