from datetime import timedelta
from django.db import models
from django.conf import settings
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils import timezone
from collections import defaultdict

# Create your models here.


class Goal(models.Model):
    """
    Represents a user's goal, tracked all the way through completion.
    Each goal has a user-selected category and urgency and importance rating.

    Attributes:
        user (User): foreign key, user details for the owner of the goal
        name (str): short label for the goal.
        created_at (date): auto-filled date when a goal is created
        description (str): brief description of the goal details.
        urgency (str): how time-sensitive the goal is, rated as urgent/not_urgent.
        importance (str): how significant the goal is, rated as important/not_important.
        timeframe (str): lifespan of the goal, marked as either 'short_term' or 'long_term'.
        planned_completion_date (date): user-set date for anticipated completion.
        started_at (date): user-set date upon starting of a goal.
        completed_at (date): user-set date upon completion of a goal.
        abandoned_at (date): user-set date upon abandonment of a goal.
        status (str): lifecycle stage of a goal - see Status choices.
        category (str): user-selected category - see Category Choices.
        abandonment_reason (str): reason for abandoning a goal.

    Business rules:
        -User sets timeframe of a goal. It is then validated  on save, by comparing the 
         duration (started_at to planned_completion_date) to DAYS_LIMIT (90 days). 
         A goal whose duration exceeds 90 days cannot be marked 'short_term', and a goal 
         within 90 days cannot be marked 'long_term'. A ValidationError is raised if the
         user's selection conflicts with the actual duration.
        -All related GoalRemediations for a goal must be resolved before a goal is marked
         completed.
        -started_at, completed_at, and abandoned_at must be provided by the user before 
         the goal can transition into the corresponding status.

    """

    DAYS_LIMIT = timedelta(days=90)

    class UrgencyChoices(models.TextChoices):
        URGENT = "urgent", "Urgent"
        NOT_URGENT = "not_urgent", "Not urgent"

    class ImportanceChoices(models.TextChoices):
        IMPORTANT = "important", "Important"
        NOT_IMPORTANT = "not_important", "Not important"

    class TimeframeChoices(models.TextChoices):
        LONG_TERM = "long_term", "Long term"
        SHORT_TERM = "short_term", "Short term"

    class StatusChoices(models.TextChoices):
        NOT_STARTED = "not_started", "Not started"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    class CategoryChoices(models.TextChoices):
        CAREER = "career", "Career"
        PERSONAL_GROWTH = "personal_growth", "Personal growth"
        UPSKILLING = "upskilling", "Upskilling"
        FINANCES = "finances", "Finances"
        HEALTH = "health", "Health"
        DIET = "diet", "Diet"
        FITNESS = "fitness", "Fitness"
        MENTAL_HEALTH = "mental_health", "Mental health"
        RECOVERY = "recovery", "Recovery"
        SPIRITUALITY = "spirituality", "Spirituality"
        CREATIVITY = "creativity", "Creativity"
        RELATIONSHIPS = "relationships", "Relationships"
        PARENTING = "parenting", "Parenting"
        TRAVEL = "travel", "Travel"
        ENTERTAINMENT = "entertainment", "Entertainment"
        OTHER = "other", "Other"

    class Meta:
        db_table = 'goals'
        constraints = [models.UniqueConstraint(
            "user", Lower("name"), name="unique_goal_per_user")]
        ordering = ['-created_at']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    urgency = models.CharField(
        choices=UrgencyChoices.choices, max_length=50, blank=True)
    importance = models.CharField(
        choices=ImportanceChoices.choices, max_length=50, blank=True)
    timeframe = models.CharField(
        choices=TimeframeChoices.choices, max_length=50, blank=True)
    planned_completion_date = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    abandoned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        choices=StatusChoices.choices, max_length=50, blank=True)
    category = models.CharField(
        choices=CategoryChoices.choices, max_length=50, blank=True)
    abandonment_reason = models.TextField(blank=True, default="")

    def __str__(self):
        return str(self.name)

    def clean(self):
        """
        Contains validation rules that will implement the applicable business logic for goals.
        It validates:
        -Correct date progression. Start date must always precede the completion, and planned completion dates.
         A goal can move from 'not started' to 'abandoned' status. Therefore, 'abandoned_at' date is not restricted
         to always be after 'started_at' date.
        -A goal whose status is 'not started' should have no start date, abandonment date, nor completion date.
        -A goal whose status is 'in progress' should have a start date , but no abandonment and completion dates.
        -A goal whose status is 'completed' should have a start date, completion date, but no abandonment date.
        -An abandonment reason is only aplicable to an abanoned goal.
        -For a goal to be marked completed, all its open challenge remediations must be remediated.
        -For a goal to be marked abandoned, all the remediations associated with its old challenges(those created before abandonment), must be remediated.
        -Short term goals must be within DAYS_LIMIT of 90 days,long term goals must exceed 90 days
        """
        errors = defaultdict(list)

        # Call the parent clean method
        try:
            super().clean()
        except ValidationError as e:
            # Check whether they are field-specific errors or general errors
            if hasattr(e, 'error_dict'):
                # add parent errors to custom clean errors by calling extend(for list errors)/append(for string errors)
                for field, messages in e.message_dict.items():
                    if isinstance(messages, list):
                        errors[field].extend(messages)
                    else:
                        errors[field].append(messages)
            else:
                # Applies to general errors
                if isinstance(e.messages, list):
                    errors[NON_FIELD_ERRORS].extend(e.messages)
                else:
                    errors[NON_FIELD_ERRORS].append(e.messages)
        # CLEAN DATE PROGRESSION
        # Start date must always come before completion date
        if self.completed_at and self.started_at:
            if self.completed_at < self.started_at:
                errors['completed_at'].append(
                    'Completion date cannot happen before start date')
        # Start date must always come before planned completion date
        if self.planned_completion_date and self.started_at:
            if self.planned_completion_date < self.started_at:
                errors['planned_completion_date'].append(
                    'Anticipated goal completion date cannot be before the start date')

        # CLEAN STATUS FIELD

        # a) Cleaning 'Not started'
        # 1. Automatically set status to not_started where both started_at and completed at are not filled
        if not self.started_at and not self.completed_at:
            if self.status != self.StatusChoices.NOT_STARTED:
                self.status = self.StatusChoices.NOT_STARTED
        # 2. Cannot be not_started if started_at exists
        if self.status == self.StatusChoices.NOT_STARTED and self.started_at:
            errors['status'].append(
                'Cannot have a start date if status is not started. Remove start date or update the correct status')
        # 3. Cannot have an abandonment date of it not started
        if self.status == self.StatusChoices.NOT_STARTED and self.abandoned_at:
            errors['abandoned_at'].append(
                'Cannot have an abandonment date if not started. Remove abanonded_at date')
        # 3. Cannot be not_started if completed_at exists
        if self.status == self.StatusChoices.NOT_STARTED and self.completed_at:
            errors['completed_at'].append(
                'Cannot have a completion date if status is not started. Remove completion date or update the correct status.')

        # b) Cleaning 'in progress'
        # 1. Enforce 'in progress' status - requires a start date
        if self.started_at and not self.completed_at:
            if self.status != self.StatusChoices.IN_PROGRESS:
                self.status = self.StatusChoices.IN_PROGRESS
        # 2. Cannot be in progress if not started
        if self.status == self.StatusChoices.IN_PROGRESS and not self.started_at:
            errors['started_at'].append(
                'Cannot be in progress if not started. Add start date')
        # 3. Cannot be in progress if abandoned
        if self.status == self.StatusChoices.IN_PROGRESS and self.abandoned_at:
            errors['abandoned_at'].append(
                'Cannot be in progress if it has an abandonment date. Remove abanonded_at date')
        # 4. Cannot be in progress if completed
        if self.status == self.StatusChoices.IN_PROGRESS and self.completed_at:
            errors['completed_at'].append(
                'Cannot have a completion date if in progress. Remove completion date')

        # c) Cleaning 'completed'
        # 1. Define rule for having a completed status
        if self.started_at and self.completed_at:
            if self.status != self.StatusChoices.COMPLETED:
                self.status = self.StatusChoices.COMPLETED
        # 2. Cannot be completed if not started
        if self.status == self.StatusChoices.COMPLETED and not self.started_at:
            errors['status'].append(
                'Cannot be completed if it has not been started')
        # 3. Cannot mark completed if completion date is missing
        if self.status == self.StatusChoices.COMPLETED and not self.completed_at:
            errors['completed_at'].append(
                'Cannot mark completed without a completion date. Enter completed_at date.')
        # 4. Cannot have abandonment date if completed:
        if self.status == self.StatusChoices.COMPLETED and self.abandoned_at:
            errors['abandoned_at'].append(
                'Cannot mark completed if it has an abandonment date. Remove abandoned at date.')
        # 5. Clean remediation before completing goals- a goal cannot be marked completed before all it's challenge remediations are remediated.
        if self.status == self.StatusChoices.COMPLETED:
            if self.pk:
                pending_remediations = ChallengeRemediation.objects.filter(  # pylint: disable=no-member
                    challenge__goal=self, remediated_at__isnull=True).count()
                if pending_remediations > 0:
                    errors['status'].append(
                        f'The goal has {pending_remediations} pending challenge remediations, ensure all are remediated before marking the goal as completed')
                    errors['completed_at'].append(
                        'Clear all challenge remediations before setting a goal completion date')

        # d) Cleaning 'abandoned'
        # 1. All rules in one, defining the status as well as handling errors where correct dates aren't input
        if self.abandoned_at:
            if not self.started_at:
                errors["started_at"].append(
                    'Cannot abandon a goal that has not been started. Include start date.')
            if self.completed_at:
                errors['completed_at'].append(
                    'An abandoned goal cannot be completed. Remove completion date.')
            self.status = self.StatusChoices.ABANDONED
        # 2. Only goals that are set as abandoned can have an abandonment reason
        if self.abandonment_reason and self.status != self.StatusChoices.ABANDONED:
            errors['abandonment_reason'].append(
                'You can only have an abandonment reason for a goal that is abandoned.')

        # 3. When abandoning, check for unresolved remediations on old challenges.
        if self.status == self.StatusChoices.ABANDONED and self.abandoned_at:
            if self.pk:
                # Check for unresolved remediations on challenges created BEFORE abandonment
                unresolved_old_remediations = ChallengeRemediation.objects.filter(  # pylint: disable=no-member
                    challenge__goal=self,
                    challenge__created_at__lt=self.abandoned_at,
                    remediated_at__isnull=True).count()
                if unresolved_old_remediations > 0:
                    errors['status'].append(
                        f'The goal has {unresolved_old_remediations} unresolved challenge remediation(s) on challenges created before abandonment, resolve them. If unresolvable, delete and update challenge remediability to "irremediable" or "remediable in future occurrences".')
                    errors['abandoned_at'].append(
                        'Resolve all remediations or update challenge remediability before abandoning.')

        # CLEAN TIMEFRAME FIELD

        if self.started_at and self.planned_completion_date:
            duration = self.planned_completion_date - self.started_at
            if self.timeframe == self.TimeframeChoices.LONG_TERM and duration < self.DAYS_LIMIT:
                errors['timeframe'].append(
                    'Cannot be long term if duration is less than 90 days')
            if self.timeframe == self.TimeframeChoices.SHORT_TERM and duration > self.DAYS_LIMIT:
                errors['timeframe'].append(
                    'Cannot be short term if duration is more than 90 days')

        if errors:
            raise ValidationError(dict(errors))

    def save(self, *args, **kwargs):
        """
        Extends the parent/default save method to run full validation before 
        writing to the database.
        Calls full_clean() on every save to ensure clean() validations are
        enforced outside of form and serializer contexts.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    # HELPER METHODS BELOW

    # To start a goal
    def start_goal(self):
        """
        Automatically starts a goal, recording start time and updating status
        to 'in progress'.
        Calls custom save(), performing necessary validations. 
        """
        self.started_at = timezone.now()
        self.status = self.StatusChoices.IN_PROGRESS
        self.save()

    # To abandon a goal
    def abandon_goal(self):
        """
        Automatically abandons a goal, recording abandinment time and updating status
        to 'abandoned'.
        Calls custom save(), performing necessary validations. 
        """
        self.abandoned_at = timezone.now()
        self.status = self.StatusChoices.ABANDONED
        self.save()

    # To complete goal
    def complete_goal(self):
        """
        Automatically completes a goal, recording completion time and updating status
        to 'completed'.
        Calls custom save(), performing necessary validations. 
        """
        self.completed_at = timezone.now()
        self.status = self.StatusChoices.COMPLETED
        self.save()

    # To reset populated goal fields to their original/default state
    # NOTE: Consider adding a method or action to undo the reset goal method
    def reset_goal(self, commit=True):
        """
        Automatically resets a goal, removing all details of a goal except for
        the user, goal name and creation time.
        Calls custom save(), performing necessary validations. 
        """
        self.description = "No description provided"
        self.urgency = ""
        self.importance = ""
        self.timeframe = ""
        self.planned_completion_date = None
        self.started_at = None
        self.completed_at = None
        self.abandoned_at = None
        self.status = ""
        self.category = ""

        if commit:
            self.save()

    # Added the below line to remove error in views.py regarding Goal not having an objects member under>> Goal.objects.all()
    objects = models.Manager()


class Challenge(models.Model):
    """
    Represents challenges associated with a goal, requiring unique challenges per goal.
    Records the remediability status of the challenges.

    Attributes:
        goal (Goal): foreign key, the goal associated with a challenge
        title (str): short label for the challenge.
        description (str): detailed description on the challenge.
        created_at (date): auto-filled date when a challenge is created
        remediability (str): ability of a challenge to be resolved- see Remediability choices.

    Business rules:
        -New challenges logged for completed or abandoned goals(those created after abandonment/completion of a goal) cannot be remediable
         currently.
        -Old challenges(created before abandonment) can only be remediable currently if all their associated remediations had already been remediated under ChallengeRemediations .
    """

    class RemediabilityChoices(models.TextChoices):
        REMEDIABLE_CURRENTLY = 'remediable_currently', 'Remediable in current goal'
        REMEDIABLE_FUTURE = 'remediable_future', 'Remediable only in future occurrences'
        IRREMEDIABLE = 'irremediable', 'Irremediable(completely unfixable)'

    class Meta:
        db_table = 'challenges'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(
            'goal', Lower('title'), name='unique_challenge_per_goal')]

    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remediability = models.CharField(
        choices=RemediabilityChoices.choices, max_length=50, blank=True)

    def __str__(self):
        return str(self.title)

    def clean(self):
        """
        Contains validation rules that will implement the applicable business logic for goal challenges.
        It validates:
        -New challenges created after abandonment or completion of a goal, must not be remediable currently. 
        -An old challenge created before a goal is abandoned /completed can maintain 'remeddiable currently' status as long as all its associated remediations are resolved.
        """
        errors = defaultdict(list)

        # Call parent clean method
        try:
            super().clean()
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                for field, messages in e.message_dict.items():
                    if isinstance(messages, list):
                        errors[field].extend(messages)
                    else:
                        errors[field].append(messages)
            else:
                if isinstance(e.messages, list):
                    errors[NON_FIELD_ERRORS].extend(e.messages)
                else:
                    errors[NON_FIELD_ERRORS].append(e.messages)

        # 1. a)Clean what should happen when a challenge is created after a goal is abandoned or completed.
        if hasattr(self, 'goal') and self.goal:
            parent_goal = self.goal
            #THe reference_time variable below ensures that we cater for both a challenge that exists(has already been saved to database, 
            # and has a created_at value), as well as a new unsaved challenge(without pk and therefore without created_at value).
            
            reference_time = self.created_at if self.pk and self.created_at else timezone.now()

            # NEW challenges (created AFTER abandonment/completion) cannot be "remediable_currently"
            if parent_goal.status == parent_goal.StatusChoices.ABANDONED:  # pylint: disable=no-member
                if reference_time > parent_goal.abandoned_at:  # pylint: disable=no-member
                    if self.remediability == self.RemediabilityChoices.REMEDIABLE_CURRENTLY:
                        errors['remediability'].append(
                            'A new challenge for an abandoned goal cannot be remediable currently. Update remediability')

            if parent_goal.status == parent_goal.StatusChoices.COMPLETED:  # pylint: disable=no-member
                if reference_time > parent_goal.completed_at:  # pylint: disable=no-member
                    if self.remediability == self.RemediabilityChoices.REMEDIABLE_CURRENTLY:
                        errors['remediability'].append(
                            'A new challenge for a completed goal cannot be remediable currently. Update remediability')

            # b) OLD challenges (created BEFORE abandonment) can stay "remediable_currently" ONLY if all remediations are resolved
            if parent_goal.status == parent_goal.StatusChoices.ABANDONED and self.pk:   # pylint: disable=no-member
                if self.created_at and self.created_at < parent_goal.abandoned_at:   # pylint: disable=no-member
                    if self.remediability == self.RemediabilityChoices.REMEDIABLE_CURRENTLY:
                        unresolved = self.challenge_remediations.filter(   # pylint: disable=no-member
                            remediated_at__isnull=True).count()
                        if unresolved > 0:
                            errors['remediability'].append(
                                f'This challenge has {unresolved} unresolved remediation(s). Either remediate them or change remediability to "Irremediable" or "Remediable for future goals".')
        if errors:
            raise ValidationError(dict(errors))

    # Overriding save method

    def save(self, *args, **kwargs):
        """
        Extends the parent/default save method to run full validation before 
        writing to the database.
        Calls full_clean() on every save to ensure clean() validations are
        enforced outside of form and serializer contexts.
        """
        self.full_clean()
        super().save(*args, **kwargs)


class Win(models.Model):
    """
    Represents successes associated with a goal, requiring unique wins per goal.

    Attributes:
        goal (Goal): Foreign key, the goal associated with a win
        title (str): Short label for the win.
        description (str): Detailed description on the win.
        created_at (date): auto-filled date when a win is created

    Business rules:
        -Wins can be logged for a goal at any point in its life cycle(status).
    """
    class Meta:
        db_table = 'wins'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(
            'goal', Lower('title'), name='unique_win_per_goal')]

    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='wins')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class ChallengeRemediation(models.Model):
    """
    Represents a resolution action taken to address a challenge associated with a goal,
    tracking it to the point of remediation.
    There should be unique remediations per challenge.

    Attributes:
        challenge (Challenge): Foreign key, the challenge associated with a remediation.
        title (str): Short label for a remediation.
        description (str): Detailed description of the remediation.
        created_at (date): auto-filled date when a challenge is created
        started_at (date): User-set date for when the remediation begins.
        due_date (date): User-set date for the anticipated resolution.
        remediated_at (date): User-set date for when the remediation is resolved/completed.

    Business rules:
        -Remediations are only associated with challenges that are remediable currently.
    """
    class Meta:
        db_table = 'remediations'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(
            'challenge', Lower('title'), name='unique_remediation_per_challenge')]

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, limit_choices_to={
                                  'remediability': 'remediable_currently'}, related_name='challenge_remediations')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    remediated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.title)

    def clean(self):
        """
        Contains validation rules that will implement the applicable business logic for challenge remediations.
        It validates:
        -Correct date progression. Start date must always precede the remediation and due dates.   
        -You cannot add a new remediation for a goal that had been marked as abandoned or completed.
        -All challenge remediations must only be associated with challenges that are remediable currently.
        """
        errors = defaultdict(list)

        # Call the parent clean method
        try:
            super().clean()
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                for field, messages in e.message_dict.items():
                    if isinstance(messages, list):
                        errors[field].extend(messages)
                    else:
                        errors[field].append(messages)
            else:
                if isinstance(e.messages, list):
                    errors[NON_FIELD_ERRORS].extend(e.messages)
                else:
                    errors[NON_FIELD_ERRORS].append(e.messages)

        # Clean date progression
        if self.started_at and self.remediated_at:
            if self.remediated_at < self.started_at:
                errors['remediated_at'].append(
                    'Cannot complete remediation before initiating it. Check remediation start date')

        if self.started_at and self.due_date:
            if self.due_date < self.started_at:
                errors['due_date'].append(
                    'Due date for remediation cannot be before start date. Recheck both dates.')

        # a) Clean that no challenge remediations should be added for challenges that are not remediable currently
        # b) Clean that no challenge remediations should be added for challenges associated with goals that are abandoned or completed

        if hasattr(self, 'challenge') and self.challenge:
            # a) Clean that no challenge remediations should be added for challenges that are not remediable currently(This is an additional guardrail in addition to the use of limit_choices_to used in the challenge field, which works on limiting the choices in the form UI only.)
            if self.challenge.remediability != self.challenge.RemediabilityChoices.REMEDIABLE_CURRENTLY:  # pylint: disable=no-member
                errors['challenge'].append(
                    'You can only add a challenge remediation if its challenge remediability is set to remediable currently')

        # b) Clean that no new challenge remediations should be added for challenges associated with goals that are abandoned or completed
            parent_goal = self.challenge.goal  # pylint: disable=no-member

            # This ensures that we only block the new remediations(raised after completion/abandonment)
            if not self.pk:
                if parent_goal.status == parent_goal.StatusChoices.ABANDONED:
                    errors['challenge'].append(
                        'The goal associated with this challenge has been marked "Abandoned", you cannot add a new challenge remediation for an abandoned goal.')
                if parent_goal.status == parent_goal.StatusChoices.COMPLETED:
                    errors['challenge'].append(
                        'The goal associated with this challenge has been marked "Completed", you cannot add a new challenge remediation for a completed goal.')

        if errors:
            raise ValidationError(dict(errors))

    def save(self, *args, **kwargs):
        """
        Extends the parent/default save method to run full validation before 
        writing to the database.
        Calls full_clean() on every save to ensure clean() validations are
        enforced outside of form and serializer contexts.
        """
        self.full_clean()
        super().save(*args, **kwargs)
