from tsuru_dashboard.admin.views import NodeInfo
from mock import patch
from django.test import TestCase
from django.test.client import RequestFactory


class NodeInfoViewTest(TestCase):
    @patch("tsuru_dashboard.auth.views.token_is_valid")
    def test_should_use_node_info_template(self, token_is_valid):
        token_is_valid.return_value = True

        factory = RequestFactory()
        request = factory.get('/')
        request.session = {'tsuru_token': 'tokentest'}

        response = NodeInfo.as_view()(request, address="http://127.0.0.1")
        self.assertIn("admin/node_info.html", response.template_name)
