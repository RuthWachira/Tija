from django.db import models  # preimported by django

# Create your models here.


class Goals(models.Model):
    name = models.CharField(max_length=255)
    # to update to dropdown later and hence adjust the field class.
    priority = models.CharField(max_length=255)
    # to update to dropdown later and hence adjust the field class.
    timeline = models.CharField(max_length=255)
    planned_completion_date = models.DateField(
        auto_now_add=True)  # to update to a calendar picker
    # to update to a calendar picker
    start_date = models.DateField(auto_now_add=True)
    progress_notes = models.CharField
    actual_completion_date = models.DateField(
        auto_now_add=True)  # to update to a calendar picker
    lessons_learnt = models.CharField
