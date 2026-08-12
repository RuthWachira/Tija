from django import forms
from .models import Goal, Challenge, Win, ChallengeRemediation


# Helper method:
def datetime_widget():
    return forms.DateTimeInput(attrs={"type": "datetime-local", "step": "1"},
                               format="%Y-%m-%dT%H:%M:%S",)


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["name", "description", "category", "timeframe", "urgency", "importance", "status", "planned_completion_date",
                  "started_at", "completed_at", "abandoned_at", "abandonment_reason"]

        _datetime_fields = ["planned_completion_date",
                            "started_at", "completed_at", "abandoned_at"]

        widgets = {
            field: datetime_widget() for field in _datetime_fields
        }


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["goal", "title", "description", "remediability"]


class WinForm(forms.ModelForm):
    class Meta:
        model = Win
        fields = ["goal", "title", "description"]


class ChallengeRemediationForm(forms.ModelForm):
    class Meta:
        model = ChallengeRemediation
        fields = ["challenge", "title", "description",
                  "started_at", "due_date", "remediated_at"]
        _datetime_fields = ["started_at", "due_date", "remediated_at"]

        widgets = {
            field: datetime_widget for field in _datetime_fields
        }
