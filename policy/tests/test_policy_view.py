from django.test import TestCase


class PolicyViewTest(TestCase):

    def test_policy(self):
        response = self.client.get("/policy/")
        self.assertEqual(200, response.status_code)
