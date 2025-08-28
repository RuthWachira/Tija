from . import views  # manually imported by me
from django.urls import path  # manually imported by me


app_name = 'goals'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:goal_id>', views.detail, name='detail')
]
