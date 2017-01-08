from django.shortcuts import render, redirect
from .models import Course, Comment
from ..login_reg.models import User
from django.core.urlresolvers import reverse
from datetime import date

def index(request):
    c = Course.objects.all()
    for i in c:
        i.created_at = i.created_at.strftime("%b. %-d %Y %-I:%M %p")
    context = {
        'courses': c
    }
    return render(request, 'courses/index.html', context)

def create(request):
    Course.objects.create(name=request.POST['name'], description=request.POST['description'])
    return redirect(reverse('courses:index'))

def confirm(request, id):
    context = {
        'course' : Course.objects.get(pk=id),
        'id' : id
    }
    return render(request, 'courses/confirm.html', context)

def destroy(request, id):
    Course.objects.get(pk=id).delete()
    return redirect(reverse('courses:index'))

def comments(request,id):
    context={
        'course' : Course.objects.get(pk=id),
        'comments' : Comment.objects.filter(course=id)
    }
    return render(request, 'courses/comment.html', context)

def new(request, id):
    if 'id' not in request.session:
        return redirect(reverse('courses:index'))
    course = Course.objects.get(pk=id)
    user = User.UserManager.get(pk=request.session['id'])
    Comment.objects.create(comment=request.POST['comment'], course = course, user=user)
    return redirect(reverse('courses:comment', kwargs={'id': id }))
