from django.test import TestCase
from django.template import Context, Template


class TestFilter(TestCase):

    def test_datetime_filter(self):
        html = '{% load filters_deploys %}'
        html += '{{ timestamp|string_to_date }}'
        template = Template(html)
        context = Context({'timestamp': '2014-02-27T17:55:34.2-03:00'})
        timestamp = "Feb. 27, 2014, 5:55 p.m."
        self.assertEqual(timestamp, template.render(context))

    def test_time_to_string_filter(self):
        html = '{% load filters_deploys %}'
        html += '{{ duration|time_to_string }}'
        template = Template(html)
        context = Context({'duration': '203902854662'})
        self.assertEqual("03m23s", template.render(context))

    def test_time_to_string_filter_with_hour(self):
        html = '{% load filters_deploys %}'
        html += '{{ duration|time_to_string }}'
        template = Template(html)
        context = Context({'duration': '7403902854662'})
        self.assertEqual("02h03m23s", template.render(context))
