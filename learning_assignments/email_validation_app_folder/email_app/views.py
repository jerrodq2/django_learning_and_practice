from django.shortcuts import render, redirect
from .models import Email

def index(request):
    if 'error' not in request.session:
        request.session['error'] = ''
    return render(request, 'email_app/index.html')

def success(request):
    context = {'emails': Email.CheckEmail.all()}
    return render(request, 'email_app/success.html', context)

def process(request):
    if request.method != 'POST':
        return redirect('/')
    request.session['error'] = ''
    request.session['success'] = ''
    check = Email.CheckEmail.checkEmail(request.POST['email'])
    if check['errors']:
        request.session['error'] = check['errors']
        return redirect('/')
    else:
        Email.CheckEmail.new(request.POST['email'])
        request.session['success'] = 'DONE!'
        return redirect('/success')

def destroy(request, id):
    Email.CheckEmail.destroy(id)
    return redirect('/success')
