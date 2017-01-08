from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

def index(request):
    return render(request, 'login_reg_app/index.html')

def reg(request):
    if request.method != 'POST':
        return redirect(reverse('logreg:index'))
    user = User.UserManager.reg(request.POST)
    if user['errors']:
        for i in user['errors']:
            messages.info(request, i)
        return redirect(reverse('logreg:index'))
    # request.session['name'] = user['name']
    request.session['id'] = user['id']
    messages.success(request, user['name'])
    return redirect(reverse('logreg:success'))

def login(request):
    if request.method != 'POST':
        return redirect(reverse('logreg:index'))
    user = User.UserManager.login(request.POST)
    if user['errors']:
        for i in user['errors']:
            messages.info(request, i)
        return redirect(reverse('logreg:index'))
    # request.session['name'] = user['name']
    request.session['id'] = user['id']
    messages.success(request, user['name'])
    return redirect(reverse('logreg:success'))

def success(request):
    return render(request, 'login_reg_app/success.html')
