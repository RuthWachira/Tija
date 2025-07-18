from django.shortcuts import render  #preimported by django
from django.http import HttpResponse  #manually imported by me
# Create your views here.


def index(request):
    return HttpResponse("Howdy! howdy! howdy to you!. Welcome aboard and set a GOAL")
