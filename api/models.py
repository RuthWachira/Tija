from django.db import models #preimported by django
from goals.models import Goal  #imported by me
from tastypie.resources import ModelResource

# Create your models here.

class GoalResource(ModelResource):
    class Meta:
        queryset = Goal.objects.all()
        resource_name = "goals"