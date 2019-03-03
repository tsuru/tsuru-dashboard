from django.test import TestCase
from django.test.client import RequestFactory
from tsuru_autoscale.app.views import IndexView

from mock import patch, Mock


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}       
      
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch.object(IndexView, "client")
    def test_index(self, fake_client, token_is_valid):
        token_is_valid.return_value = True

        expected_instance = {"Name": "myinstance", "Apps": ["myapp"]}
        fake_client.instance.list.return_value = [expected_instance]
        fake_client.wizard.get.return_value.status_code = 200

        response = IndexView.as_view()(self.request, app="myapp")
        self.assertIn("app/index.html", response.template_name)
        self.assertIn('instance', response.context_data)
        self.assertIn('auto_scale', response.context_data)
        self.assertIn('app', response.context_data)
        self.assertIn('events', response.context_data)
        self.assertEqual(expected_instance, response.context_data['instance'])
        IndexView.client.instance.list.assert_called()
        IndexView.client.wizard.get.assert_called_with("myinstance")
        IndexView.client.wizard.events.assert_called_with("myinstance")

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch.object(IndexView, "client")
    def test_index_instance_not_found(self, fake_client, token_is_valid):
        token_is_valid.return_value = True

        fake_client.instance.list.return_value = []

        response = IndexView.as_view()(self.request, app="myapp")

        self.assertIn("app/index.html", response.template_name)
        IndexView.client.instance.list.assert_called()
        IndexView.client.wizard.get.assert_not_called()
        IndexView.client.wizard.events.assert_not_called()