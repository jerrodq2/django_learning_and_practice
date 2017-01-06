from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return render(request, 'disappearing_ninjas/index.html')
def ninja(request):
    return render(request, 'disappearing_ninjas/ninja.html')

def color(request, color):
    options = {
        'blue': 'Leonard',
        'red' : 'Raphael',
        'orange': 'Michelangelo',
        'purple': 'Donatello'
    }
    if color in options:
        context = {'name': options[color]}
    else:
        context = {'name': 'MEGAN FOX'}
    return render(request, 'disappearing_ninjas/color.html', context)

# Create your views here.
