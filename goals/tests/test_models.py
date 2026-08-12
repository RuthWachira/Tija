"""
Contains tests for the app models.
"""

# imported by me. Custom test file(removed the original tests.py file)
from django.test import TestCase
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from ..models import Goal, Challenge, Win, ChallengeRemediation


class GoalModelTest(TestCase):
    """
    Test class where we shall have assorted tests for the Goal model.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="Nyagaki", password="Nyagaks123"
        )
        cls.goal = Goal.objects.create(
            user=cls.user,
            name="Master model testing",
            urgency=Goal.UrgencyChoices.URGENT,
            importance=Goal.ImportanceChoices.IMPORTANT,
            timeframe=Goal.TimeframeChoices.SHORT_TERM,
            started_at=timezone.now(),
            planned_completion_date=timezone.now()+timedelta(days=10),
            status=Goal.StatusChoices.IN_PROGRESS,
            category=Goal.CategoryChoices.CAREER
        )
# THE 3 TESTS BELOW WILL USE THE DATA IN SETUPTESTDATA CREATED ABOVE

    def test_goal_creation(self):  # This is a unit test
        self.assertEqual(self.goal.name, "Master model testing")
        self.assertIsNone(self.goal.completed_at)
        self.assertGreater(self.goal.planned_completion_date,
                           self.goal.started_at)

    def test_name_str_representation(self):
        self.assertEqual(str(self.goal), "Master model testing")


# THE BELOW TESTS RELATE TO UNEXPECTED SCENARIOS. THEY DO NOT RELY ENTIRELY ON THE SETUPTESTDATA

    # This is a data integrity test with


    def test_invalid_entry_in_choices_raises_error(self):
        goal = Goal(user=self.user, status="manually_typed_status")
        with self.assertRaises(ValidationError) as cm:
            goal.save()
        self.assertIn("status", cm.exception.message_dict)

    def test_date_progression(self):  # This is a unit logic test
        goal = Goal(
            user=self.user,
            name="Learn unit testing",
            started_at=timezone.now(),
            completed_at=timezone.now()-timedelta(days=10)
        )
        with self.assertRaises(ValidationError) as cm:
            goal.save()
        self.assertIn("completed_at", cm.exception.message_dict)

    # This is a data integrity test
    def test_goal_uniqueness_per_user(self):
        duplicate = Goal(user=self.user, name="master Model testing",
                         category=Goal.CategoryChoices.CREATIVITY)
        with self.assertRaises(ValidationError) as cm:
            duplicate.save()
        self.assertIn(NON_FIELD_ERRORS, cm.exception.message_dict)

    def test_abandonment_reason(self):  # This is a data integrity test
        goal = Goal(user=self.user,
                    status=Goal.StatusChoices.IN_PROGRESS,
                    abandonment_reason="Lack of learning resources")
        with self.assertRaises(ValidationError) as cm:
            goal.save()
        self.assertIn("abandonment_reason", cm.exception.message_dict)


class ChallengeModelTest(TestCase):
    """
    Test class where we shall have assorted tests for the Challenge model.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="Ruth", password="rutsy123")
        cls.goal = Goal.objects.create(
            user=cls.user, name="create an agent tool")
        cls.challenge = Challenge.objects.create(  # pylint: disable=no-member
            goal=cls.goal, title="Skills gap in AI", remediability=Challenge.RemediabilityChoices.REMEDIABLE_CURRENTLY)

    def test_unique_challenges_per_goal(self):
        duplicate_challenge = Challenge(
            goal=self.goal, title="Skills gap in AI")
        with self.assertRaises(ValidationError) as cm:
            duplicate_challenge.save()
        self.assertIn(NON_FIELD_ERRORS, cm.exception.message_dict)

    def test_remediability_for_completed_goals(self):
        completed_goal = Goal.objects.create(
            user=self.user, name="Create personal dashboard",
            started_at=timezone.now()-timedelta(days=10),
            status=Goal.StatusChoices.COMPLETED,
            completed_at=timezone.now()-timedelta(days=5))
        new_challenge = Challenge(goal=completed_goal, title="Took too long",
                                  remediability=Challenge.RemediabilityChoices.REMEDIABLE_CURRENTLY)

        with self.assertRaises(ValidationError) as cm:
            new_challenge.save()
        self.assertIn("remediability", cm.exception.message_dict)


class WinModelTest(TestCase):
    """
    Test class where we shall have assorted tests for the Win model.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="Ruth", password="1234")
        cls.goal = Goal.objects.create(
            user=cls.user, name="Create model tests in 1 week")
        cls.win = Win.objects.create(  # pylint: disable=no-member
            goal=cls.goal, title="Managed to create views tests int he week too")

    def test_win_creation(self):
        self.assertEqual(
            self.win.title, "Managed to create views tests int he week too")

    def test_str_representation(self):
        self.assertEqual(
            str(self.win), "Managed to create views tests int he week too")


class ChallengeRemediationModelTest(TestCase):
    """
    Test class where we shall have assorted tests for the Win model.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="Ruth", password="1234")
        cls.goal = Goal.objects.create(
            user=cls.user, name="Create personal dashboard")
        cls.challenge = Challenge.objects.create(goal=cls.goal, title="No powerBI subscription",  # pylint: disable=no-member
                                                 remediability=Challenge.RemediabilityChoices.REMEDIABLE_CURRENTLY)

    def test_remediations_for_invalid_remediability(self):
        """
        Test whether validation error set in clean method in models is caught, if a remediation is added to a challenge which is not remediable currently.
        Note: Our business logic dictates that remediataions can only be added if a challenge is remediable_currently.
        """
        challenge = Challenge.objects.create(goal=self.goal, title="Laptop crashed",  # pylint: disable=no-member
                                             remediability=Challenge.RemediabilityChoices.IRREMEDIABLE)
        remediation = ChallengeRemediation(
            challenge=challenge, title="Trying to source new laptop")

        with self.assertRaises(ValidationError) as cm:
            remediation.save()
        self.assertIn("challenge", cm.exception.message_dict)

    def test_remediation_dates_progression(self):
        """
        Test what happens when correst date progression is violated. I.e if errors are raised when the remediation date is before the start date.
        """
        remediation = ChallengeRemediation(title="Obtained powerBI subscriprion", challenge=self.challenge, started_at=timezone.now(),
                                           remediated_at=timezone.now() - timedelta(days=5))
        with self.assertRaises(ValidationError) as cm:
            remediation.save()
        self.assertIn("remediated_at", cm.exception.message_dict)
