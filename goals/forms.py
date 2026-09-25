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
            **{field: datetime_widget() for field in _datetime_fields},
            "description": forms.Textarea(attrs={"rows": 4}),
            "abandonment_reason": forms.Textarea(attrs={"rows": 5})
        }

        help_texts = {
            "description": "Briefly describe your goal",
            "abandonment_reason": "Describe reason(s) for abandoning your goal"
        }


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["goal", "title", "description", "remediability"]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4})
        }

        help_texts = {
            "title": "Setback/difficulty encountered in the execution and/or achievement of the goal"
        }

    def __init__(self, *args, user=None, goal=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['goal'].queryset = Goal.objects.filter(user=user)

        if goal is not None:
            self.fields["goal"].initial = goal
            self.fields["goal"].widget = forms.HiddenInput()
            self.fields["goal"].disabled = True


class WinForm(forms.ModelForm):
    class Meta:
        model = Win
        fields = ["goal", "title", "description"]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4})
        }

        help_texts = {
            "title": "Wins are moments of progress you want to remember e.g a milestone, a breakthrough, or just a"
            " good day's effort toward this goal. you don't have to wait until the goal is fully complete."
        }

    def __init__(self, *args, user=None, goal=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["goal"].queryset = Goal.objects.user(user=user)

        if goal is not None:
            self.fields["goal"].initial = goal
            self.fields["goal"].widget = forms.HiddenInput()
            self.fields["goal"].disabled = True


class ChallengeRemediationForm(forms.ModelForm):
    class Meta:
        model = ChallengeRemediation
        fields = ["challenge", "title", "description",
                  "started_at", "due_date", "remediated_at"]
        _datetime_fields = ["started_at", "due_date", "remediated_at"]

        widgets = {
            field: datetime_widget for field in _datetime_fields
        }

        help_texts = {
            "title": "Actions taken towards resolving a challenge faced when executing a goal",
            "description": "Expound briefly on the remediation title provided above",
            "started_at": "Date when you started resolving for a challenge",
            "due_date": "Target/anticipated date of finalising the remediation",
            "remediated_at": "Actual date when you finalised resolving the challenge"
        }
