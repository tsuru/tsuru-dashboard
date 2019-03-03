from django.test import TestCase
from django.test.client import RequestFactory
from mock import patch, Mock

from tsuru_autoscale.instance.views import ListInstance, InstanceInfo


class ListInstanceTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}       

    @patch.object(ListInstance, "client")
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_list(self, token_is_valid, fake_client):
        token_is_valid.return_value = True
        
        expected_instance = [{"Name": "myinstance"}]
        fake_client.instance.list.return_value = expected_instance

        response = ListInstance.as_view()(self.request)

        self.assertIn("instance/list.html", response.template_name)
        self.assertIn('list', response.context_data)
        self.assertEqual(expected_instance, response.context_data['list'])
        ListInstance.client.instance.list.assert_called()


class InstanceInfoTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}       

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch.object(InstanceInfo, "client")
    def test_get_without_alarms(self, fake_client, token_is_valid):
        token_is_valid.return_value = True

        json_mock = Mock()
        json_mock.json.return_value = {"Name": "instance"}
        fake_client.instance.get.return_value = json_mock

        aresponse = Mock()
        aresponse.json.return_value = None
        fake_client.instance.alarms_by_instance.return_value = aresponse

        response = InstanceInfo.as_view()(self.request, name="myinstance")

        self.assertIn("instance/get.html", response.template_name)
        self.assertIn('item', response.context_data)
        self.assertIn('alarms', response.context_data)
        self.assertIn('events', response.context_data)
        InstanceInfo.client.instance.get.assert_called_with("myinstance")
        InstanceInfo.client.instance.alarms_by_instance.assert_called_with("myinstance")
        InstanceInfo.client.event.list.assert_not_called()

    @patch("tsuru_dashboard.auth.views.token_is_valid")
    @patch.object(InstanceInfo, "client")
    def test_get(self, fake_client, token_is_valid):
        token_is_valid.return_value = True
        
        json_mock = Mock()
        json_mock.json.return_value = {"Name": "myinstance"}
        fake_client.instance.get.return_value = json_mock

        response = InstanceInfo.as_view()(self.request, name="myinstance")

        self.assertIn("instance/get.html", response.template_name)
        self.assertIn('item', response.context_data)
        self.assertIn('alarms', response.context_data)
        self.assertIn('events', response.context_data)
        InstanceInfo.client.instance.get.assert_called_with("myinstance")
