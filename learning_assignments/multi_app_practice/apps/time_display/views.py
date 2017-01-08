from django.shortcuts import render
from time import strftime, localtime

# Create your views here.
def index(request):
    context = {
        'time': strftime('%h %d, %Y %I:%M %p', localtime()),
    }
    return render(request, 'time_app/index.html', context)
