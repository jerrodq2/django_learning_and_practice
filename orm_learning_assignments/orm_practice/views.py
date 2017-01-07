from django.shortcuts import render, redirect
from .models import Blog, Comment

def index(request):
    context = {
        'blogs': Blog.objects.all()
    }
    return render(request, 'practice/index.html', context)

def blog(request):
    if request.method != 'POST':
        return redirect('/')
    # USING ORM
    Blog.objects.create(title=request.POST['title'], blog=request.POST['blog'])
    # insert into blogs (title, blog) values (title, blog)  automatically does created at and updated_at

    return redirect('/')

def comment(request, id):
    if request.method != 'POST':
        return redirect('/')
    blog = Blog.objects.get(pk=id)
    Comment.objects.create(comment=request.POST['comment'], blog=blog)
    # inserts into comment, with blog as the ForeignKey

    return redirect('/')
