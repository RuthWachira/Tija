from django.db import models  # preimported by django
from django.contrib.auth.models import User

# Create your models here.


class Goals(models.Model):
    TIMEFRAME_CHOICES = [
        ("long-term", "Long-term"),
        ("short-term", "Short-term")
    ]
    STATUS_CHOICES = [
        ("not started", "Not started"),
        ("in progress", "In progress"),
        ("completed", "Completed")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField(default="No description provided")
    priority = models.CharField(max_length=255)  # i.e urgent and important etc
    # to update to dropdown later  with choice selection and hence adjust the field class.
    timeframe = models.CharField(
        choices=TIMEFRAME_CHOICES, max_length=255)
    # i.e long-term or short-term
    planned_completion_date = models.DateField(null=True, blank=True)
    # to update to a calendar picker widget
    start_date = models.DateField(null=True, blank=True)
    # to update to a calendar picker widget
    # to update to a calendar picker widget
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=255)


class Analysis(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    challenges = models.TextField(default="No challenge indicated")
    lessons = models.TextField(default="No lesson indicated")
    proposed_action = models.TextField(default="No proposed action")
