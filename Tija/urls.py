"""
URL configuration for Tija project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # preimported by django
from django.urls import path, include
# path was preimported by django, I however added the 'include' function
from . import views
from api.models import GoalResource

goal_resource = GoalResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goals/', include('goals.urls')),
    path('', views.home),
    path('api/', include(goal_resource.urls))
]
