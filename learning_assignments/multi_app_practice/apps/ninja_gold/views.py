from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import random


def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'activity' not in request.session:
        request.session['activity'] = []
    return render(request, 'ninja_gold/index.html')

def process(request, place):
    session_list = request.session['activity']
    string = ''
    lost_gain = 'gain'
    if place == 'farm':
        num = random.randint(10 , 20)
        string = 'Earned {} gold from the Farm!'.format(num)
    if place == 'cave':
        num = random.randint(5 , 10)
        string = 'Earned {} gold from the Cave!'.format(num)
    if place == 'house':
        num = random.randint(2, 5)
        string = 'Earned {} gold from the House!'.format(num)
    if place == 'casino':
        chance = random.randint(0, 1)
        num = random.randint(0, 50)
        if chance:
            string = 'Earned {} gold from the Casino!'.format(num)
        else:
            string = 'Lost {} gold from the Farm!'.format(num)
            lost_gain = 'lost'
    if lost_gain == 'gain':
        request.session['gold'] += num
    else:
        request.session['gold'] -= num
    session_list.append({'string': string, 'lost_gain':lost_gain })
    request.session['activity'] = session_list
    return redirect(reverse('ninja:index'))

def reset(request):
    request.session['gold'] = 0
    request.session['activity'] = []
    return redirect(reverse('ninja:index'))

# Create your views here.
