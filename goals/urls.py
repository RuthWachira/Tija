from . import views #manually imported by me
from django.urls import path #manually imported by me

urlpatterns = [
path('', views.index, name = 'index')
]