from django.shortcuts import render
from time import strftime, localtime

# Create your views here.
def index(request):
    context = {
        'time': strftime('%h %d, %Y %I:%M %p', localtime()),
    }
    return render(request, 'time_app/index.html', context)



# ANSWERSHEET BELOW

# from django.shortcuts import render, HttpResponse
# import datetime
#
# # Create your views here.
# def index(request):
#     i = datetime.datetime.now()
#     currentDateTime = ("%s/%s/%s" % (i.day,i.month,i.year)) + (" %s:%s:%s" % (i.hour,i.month,i.second))
#
#     context={
#     "currentDateTime":currentDateTime
#     }
#     return render(request, 'timedisplay/index.html', context)
