from django.test import TestCase
from django.urls import reverse, resolve


class TestUrls(TestCase):

    def test_list_service_url(self):
        resolver = resolve('/services/')
        self.assertEqual(resolver.view_name, 'service-list')

    def test_service_detail_url(self):
        tests = [
            ["myservice", "myinstance"],
            ["my-service", "myinstance"],
            ["my_service", "myinstance"],
            ["my::service", "myinstance"],
        ]

        for test in tests:
            url = reverse('service-detail', args=test)
            self.assertEqual(url, '/services/'+test[0]+'/instances/'+test[1]+'/')
            resolver = resolve(url)
            self.assertEqual(resolver.view_name, 'service-detail')

    def test_service_add_url(self):
        tests = [
            ["myservice"],
            ["my-service"],
            ["my_service"],
            ["my::service"],
        ]

        for test in tests:
            url = reverse('service-add', args=test)
            self.assertEqual(url, '/services/'+test[0]+'/add/')
            resolver = resolve(url)
            self.assertEqual(resolver.view_name, 'service-add')

    def test_service_remove_url(self):
        tests = [
            ["myservice", "myinstance"],
            ["my-service", "myinstance"],
            ["my_service", "myinstance"],
            ["my::service", "myinstance"],
        ]

        for test in tests:
            url = reverse('service-remove', args=test)
            self.assertEqual(url, '/services/'+test[0]+'/instances/'+test[1]+'/remove/')
            resolver = resolve(url)
            self.assertEqual(resolver.view_name, 'service-remove')

    def test_service_bind_url(self):
        tests = [
            ["myservice", "myinstance"],
            ["my-service", "myinstance"],
            ["my_service", "myinstance"],
            ["my::service", "myinstance"],
        ]

        for test in tests:
            url = reverse('bind', args=test)
            self.assertEqual(url, '/services/'+test[0]+'/instances/'+test[1]+'/bind/')
            resolver = resolve(url)
            self.assertEqual(resolver.view_name, 'bind')

    def test_service_unbind_url(self):
        tests = [
            ["myservice", "myinstance", "myapp"],
            ["my-service", "myinstance", "myapp"],
            ["my_service", "myinstance", "myapp"],
            ["my::service", "myinstance", "myapp"],
        ]

        for test in tests:
            url = reverse('unbind', args=test)
            self.assertEqual(url, '/services/'+test[0]+'/instances/'+test[1]+'/'+test[2]+'/unbind/')
            resolver = resolve(url)
            self.assertEqual(resolver.view_name, 'unbind')
