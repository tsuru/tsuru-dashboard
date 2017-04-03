from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory

from tsuru_dashboard.admin.views import NodeAdd

import json


class FakeTsuruClient(object):
    def __init__(self, error=""):
        create = Mock()
        attrs = {"iter_lines.return_value": [json.dumps({"Message": "", "Error": error})]}
        create.configure_mock(**attrs)

        self.nodes = Mock()
        attrs = {"create.return_value": create}
        self.nodes.configure_mock(**attrs)


class NodeAddViewTest(TestCase):
    @patch.object(NodeAdd, "client", FakeTsuruClient(error="something is wrong"))
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_register_false(self, token_is_valid):
        token_is_valid.return_value = True

        request = RequestFactory().post('/', data={"key": "value", "register": "true"})
        request.session = {'tsuru_token': 'tokentest'}
        response = NodeAdd.as_view()(request)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, "something is wrong")

    @patch.object(NodeAdd, "client", FakeTsuruClient())
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_view_register_true(self, token_is_valid):
        token_is_valid.return_value = True

        request = RequestFactory().post('/', data={"key": "value", "register": "true"})
        request.session = {'tsuru_token': 'tokentest'}

        response = NodeAdd.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Node was successfully created")
