from django.test import TestCase
from django.urls import resolve


class TestAdminUrls(TestCase):

    def test_urls(self):
        tests = [
            ["/", "pool-list"],
            ["/192.168.1.1/containers/", "node-info-json"],
            ["/192.168.1.1/", "node-info"],
            ["/deploys/abc123/", "deploy-info"],
            ["/deploys/", "list-deploys"],
            ["/healing/", "list-healing"],
            ["/node/192.168.1.1:8785/remove/", "node-remove"],
            ["/node/add/", "node-add"],
            ["/pool/mypool/rebalance/", "pool-rebalance"],
            ["/pool/mypool/", "pool-info"],
            ["/templates.json", "template-list-json"],
        ]

        for test in tests:
            resolver = resolve("/admin" + test[0])
            self.assertEqual(resolver.view_name, test[1])
