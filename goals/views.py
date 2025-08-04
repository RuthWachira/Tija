from django.shortcuts import render  # preimported by django
from django.http import HttpResponse  # manually imported by me
from .models import Goal
# Create your views here.


def index(request):
    # return HttpResponse("Howdy! howdy! howdy to you!. Welcome aboard and set a GOAL")   #initial view before updating it to display goal names
    goals = Goal.objects.all()   #error does not affect runtime, can be solved by installing pylint
    goal_names = [x.name for x in goals]
    return HttpResponse(','.join(goal_names))
