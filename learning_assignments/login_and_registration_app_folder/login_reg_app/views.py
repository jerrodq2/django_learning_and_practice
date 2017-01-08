from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login_reg_app/index.html')

def reg(request):
    if request.method != 'POST':
        return redirect('/')
    user = User.UserManager.reg(request.POST)
    if user['errors']:
        for i in user['errors']:
            messages.info(request, i)
        return redirect('/')
    # request.session['name'] = user['name']
    messages.success(request, user['name'])
    return redirect('/success')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    user = User.UserManager.login(request.POST)
    if user['errors']:
        for i in user['errors']:
            messages.info(request, i)
        return redirect('/')
    # request.session['name'] = user['name']
    messages.success(request, user['name'])
    return redirect('/success')

def success(request):
    return render(request, 'login_reg_app/success.html')
