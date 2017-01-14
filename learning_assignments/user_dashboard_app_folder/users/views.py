from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Message, Comment


#MAIN ROUTES***********************************
def index(request):
    context = {'users' : User.objects.all()}
    return render(request, 'users/index.html', context)

def admin(request):
    context = {'users' : User.objects.all()}
    return render(request, 'users/admin.html', context)

def destroy(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if not request.session['admin']:
        return redirect(reverse('users:index'))
    User.objects.filter(pk=id).delete()
    return redirect(reverse('users:admin'))


#NEW USER ROUTES***********************************
def new(request):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if not request.session['admin']:
        return redirect(reverse('users:index'))
    return render(request, 'users:new.html')

def create(request):
    if request.method != 'POST':
        return redirect(reverse('users:new'))
    if not request.session['admin']:
        return redirect(reverse('users:index'))
    user = User.objects.register(request.POST)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
        return redirect(reverse('users:new'))
    return redirect(reverse('users:admin'))


#EDIT USER ROUTES***********************************
def edit(request):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    context = {
        'user': User.objects.values('email', 'first_name', 'last_name', 'description').get(pk=request.session['id'])
    }
    return render(request, 'users/edit.html', context)

def edit_info(request):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    user = User.objects.edit_main_info(request.POST, request.session['id'])
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
    return redirect(reverse('users:edit'))

def edit_description(request):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    user = User.objects.edit_description(request.POST, request.session['id'])
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
    return redirect(reverse('users:edit'))

def edit_password(request):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    user = User.objects.edit_password(request.POST, request.session['id'])
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
    return redirect(reverse('users:edit'))



#ADMIN EDIT USER ROUTES***********************************
def admin_edit(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if not request.session['admin']:
        return redirect(reverse('users:index'))
    context = {
        'user': User.objects.values('email', 'first_name', 'last_name', 'id', 'admin').get(pk=id)
    }
    return render(request, 'users/admin_edit.html', context)

def admin_edit_info(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if not request.session['admin']:
        return redirect(reverse('users:index'))
    if request.method != 'POST':
        return redirect(reverse('users:admin_edit', kwargs = {'id': id}))
    user = User.objects.admin_main_info(request.POST, id)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
    return redirect(reverse('users:admin_edit', kwargs = {'id': id}))


def admin_edit_password(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if not request.session['admin']:
        return redirect(reverse('users:index'))
    if request.method != 'POST':
        return redirect(reverse('users:admin_edit', kwargs = {'id': id}))
    user = User.objects.admin_edit_password(request.POST, id)
    if user['errors']:
        for error in user['errors']:
            messages.info(request, error)
    return redirect(reverse('users:admin_edit', kwargs = {'id': id}))




#SHOW AND MESSAGE ROUTES***********************************
def show(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    user = User.objects.show(id)
    context = {
        'user': user['user'],
        'message': user['messages']
    }
    return render(request, 'users/show.html', context)

def message(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if request.method != 'POST':
        return redirect(reverse('users:show', kwargs = {'id': id}))
    message = Message.objects.new(request.POST, id, request.session['id'])
    if message['errors']:
        for error in message['errors']:
            messages.info(request, error)
    return redirect(reverse('users:show', kwargs = {'id': id}))


def comment(request, uid, mid):
    if not 'id' in request.session:
        return redirect(reverse('login_reg:index'))
    if request.method != 'POST':
        return redirect(reverse('users:show', kwargs = {'id': uid}))
    comment = Message.objects.new_comment(request.POST, uid, request.session['id'], mid)
    if comment['errors']:
        for error in comment['errors']:
            messages.info(request, error)
    return redirect(reverse('users:show', kwargs = {'id': uid}))
