from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return render(request, 'survey_form_app/index.html')

def process(request):
    print '***********'
    print request.method
    if request.method != "POST":
        return redirect('/')
    if 'count' not in request.session:
        request.session['count'] = 1
    else:
        request.session['count'] += 1
    request.session['info'] = request.POST
    return redirect('/result')

def result(request):
    return render(request, 'survey_form_app/result.html')
