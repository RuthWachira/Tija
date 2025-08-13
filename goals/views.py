from django.shortcuts import render  # preimported by django
from django.http import HttpResponse  # manually imported by me
from .models import Goal
# Create your views here.


def index(request):
    # return HttpResponse("Howdy! howdy! howdy to you!. Welcome aboard and set a GOAL")   #initial view before updating it to display goal names
    # pylint error on Goal.objects does not affect runtime, can be solved by installing pylint django.
    goals = Goal.objects.all()
    # goal_names = [x.name for x in goals]  #commented out to keep track, we incorporated initial html template rendering afterwards.
    # return HttpResponse(','.join(goal_names))  #initial view before updating to initial html template rendering
    # return render(request, 'index.html')  #initial rendering that only read the testing text typed on the index.html i.e Hello world
    return render(request, 'index.html', {'goals': goals})
