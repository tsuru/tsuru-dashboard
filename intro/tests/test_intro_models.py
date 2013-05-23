from django.test import TestCase

from intro.models import Intro


class IntroTest(TestCase):
    def test_model(self):
        intro = Intro.objects.create(email="email@domain.com")
        retrieve = Intro.objects.get(email=intro.email)
        self.assertEqual(intro.email, retrieve.email)
