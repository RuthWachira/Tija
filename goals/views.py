from django.shortcuts import render, get_object_or_404  # render > for FBVs
from .forms import GoalForm, ChallengeForm, WinForm, ChallengeRemediationForm
from .models import Goal, Challenge, Win, ChallengeRemediation
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required # login_required > for FBVs

# Create your views here.

# OLD VIEWS BELOW

def index(request):
    # return HttpResponse("Howdy! howdy! howdy to you!. Welcome aboard and set a GOAL")   #initial view before updating it to display goal names
    # pylint error on Goal.objects does not affect runtime, can be solved by installing pylint django.
    goals = Goal.objects.all()
    # goal_names = [x.name for x in goals]  #commented out to keep track, we incorporated initial html template rendering afterwards.
    # return HttpResponse(','.join(goal_names))  #initial view before updating to initial html template rendering
    # return render(request, 'index.html')  #initial rendering that only read the testing text typed on the index.html i.e Hello world
    return render(request, 'goals/index.html', {'goals': goals})


def detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    return render(request, 'goals/detail.html', {'goal': goal})


# NEW CLASS BASED VIEWS BELOW
# # custom mixin to be shared across the views
class ModelCleanErrorMixin:
    """
    Contains reusable overidden form_valid() function. For any CreateView/UpdateView whose model raises
    ValidationError from a custom clean()/save(). Catches errors that Django's parent form.is_valid() 
    couldn't catch because some fields, like 'user' or a locked parent FK, are excluded from form-level
    validation, as they have been excluded from form fields.
    """

    def form_valid(self, form):
        try:
            self.object = form.save()
        except ValidationError as e:
            for field, messages in e.message_dict.items():
                form.add_errors(
                    field if field in form.fields else None, messages)
            return self.form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())


# All Goal related views go here. Includes:
#  1.) viewing >>list, detail
#  2.) Editing >>Create, update, delete
#  3.) To do -Extras from model helper methods>> start goal, complete goal, abandon goal, reset goal
#      (implement this both from goal detail as well as from dashboard/a neutral point)


class GoalListView(LoginRequiredMixin, ListView):
    model = Goal

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalDetailView(LoginRequiredMixin, DetailView):
    model = Goal

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):
    model = Goal
    form_class = GoalForm
    # revisit url name once done with urls
    success_url = reverse_lazy("goal-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalUpdateView(LoginRequiredMixin, ModelCleanErrorMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    # revisit url name once done with urls
    success_url = reverse_lazy("goal-list")

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalDeleteView(LoginRequiredMixin, ModelCleanErrorMixin, DeleteView):
    model = Goal
    success_url = reverse_lazy("goal-list")

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


# All Challenge related views go here. includes:
#  .) Editing >>Create, update, delete. Challenges will be created through 2 main entry points:
#               a) From an existing goal. Hence will exist in the existing Goal's detail view/page
#               b) Independent view - adding a challenge from an independent location such as the dashboard,
#                  without initial access to a goal

# Editing views:
# a) Goal scoped view - adding a challenge directly from within a goal.
class GoalChallengeCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):
    """
    This view allows a challenge to be created directly from an open goal, which is already known to the url.
    """
    model = Challenge
    form_class = ChallengeForm

    def dispatch(self, request, *args, **kwargs):
        self.goal = get_object_or_404(
            Goal, pk=kwargs["goal_pk"], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["goal"] = self.goal
        return kwargs

    def get_success_url(self):
        return reverse_lazy("goal-detail", kwargs={"pk": self.goal.pk})


# b) Independent view - adding a challenge from an independent location such as the dashboard, without initial access to a goal
class ChallengeCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):
    """
    This view caters for a challlenge that will be created form an independent location e.g from the dashboard
    ,not directly from a goal url.
    """
    model = Challenge
    form_class = ChallengeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("goal-detail", kwargs={"pk": self.object.goal.pk})


class ChallengeUpdateView(LoginRequiredMixin, ModelCleanErrorMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm

    def get_queryset(self):
        return Challenge.objects.filter(goal__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("goal-detail", kwargs={"pk": self.object.goal.pk})


class ChallengeDeleteView(LoginRequiredMixin, ModelCleanErrorMixin, DeleteView):
    model = Challenge

    def get_queryset(self):
        return Challenge.objects.filter(goal__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(Goal, kwargs={"pk": self.object.goal.pk})

# All Win related views go here. includes:
#  2.) Editing >>Create, update, delete


class GoalWinCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):
    model = Win
    form_class = WinForm

    def dispatch(self, request, *args, **kwargs):
        self.goal = get_object_or_404(
            Goal, pk=kwargs["goal_pk"], user=self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["goal"] = self.goal
        return kwargs

    def get_success_url(self):
        return reverse_lazy("goal-detail", kwargs={"pk": self.goal.pk})


class WinCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):
    model = Win
    form_class = WinForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("goal-detail", kwargs={"pk": self.object.goal.pk})


class WinUpdateView(LoginRequiredMixin, ModelCleanErrorMixin, UpdateView):
    model = Win
    form_class = WinForm

    def get_queryset(self):
        return Win.objects.filter(goal__user=self.request.user)


class WinDeleteView(LoginRequiredMixin, ModelCleanErrorMixin, DeleteView):
    model = Win

    def get_queryset(self):
        return Win.objects.filter(goal__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("goal-detail", kwargs={"pk": self.object.goal.pk})

# All Challenge Remediation related views go here. includes:
#  1.) Editing >>Create, update, delete


class ChallengeRemediationCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):
    model = ChallengeRemediation
    form_class = ChallengeRemediationForm


# class RemediationCreateView(LoginRequiredMixin, ModelCleanErrorMixin, CreateView):


# class ChallengeRemediationUpdateView(LoginRequiredMixin, ModelCleanErrorMixin, UpdateView):


# class ChallengeRemediationDeleteView(LoginRequiredMixin, ModelCleanErrorMixin, DeleteView):
