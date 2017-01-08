from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import random, string
string.letters

def index(request):
    request.session['random'] = ''
    for i in range(14):
        lett = random.choice(string.letters)
        request.session['random'] += lett
    if ('count' in request.session) != True:
        request.session['count'] = 1
    context = {
        'string' : request.session['random'],
        'count' : request.session['count']
    }
    return render(request, 'random_word/index.html', context)

def reset(request):
    request.session['count'] += 1
    return redirect(reverse('random:index'))
