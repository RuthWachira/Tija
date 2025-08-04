from django.db import models  # preimported by django
from django.contrib.auth.models import User  # manually imported by me

# Create your models here.


class Goal(models.Model):
    class meta:
        db_table = 'goals'
    TIMEFRAME_CHOICES = [
        ("long-term", "Long-term"),
        ("short-term", "Short-term"),
    ]
    STATUS_CHOICES = [
        ("not started", "Not started"),
        ("in progress", "In progress"),
        ("completed", "Completed"),
    ]
    PRIORITY_CHOICES = [
        ("urgent, important", "Urgent and important (Immediate action needed)"),
        ("urgent, not important", "Urgent and  not important (Schedulable)"),
        ("not urgent, important", "Not urgent but important (Delegatable)"),
        ("not urgent, not important", "Not urgent and not important (Eliminatable)"),

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(unique=True, max_length=255)
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField(default="No description provided")
    # i.e urgent and important etc
    priority = models.CharField(
        choices=PRIORITY_CHOICES, max_length=255, null=True)
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

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    class meta:
        db_table = 'analysis'

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    date_created = models.DateField(auto_now_add=True)
    challenges = models.TextField(default="No challenge indicated")
    lessons = models.TextField(default="No lesson indicated")
    proposed_action = models.TextField(default="No proposed action")

    def __str__(self):
        return str(self.title)
