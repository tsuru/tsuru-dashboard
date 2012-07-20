from django.test import TestCase

from auth.views import AddUserToTeam, LoginRequiredView


class AddUserToTeamViewTest(TestCase):

    def test_should_require_login_to_add_user_to_team(self):
        assert issubclass(AddUserToTeam, LoginRequiredView)