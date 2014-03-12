from django.test import TestCase
from django.template import Context, Template


class TestFilter(TestCase):

    def test_datetime_filter(self):

        html = '{% load deploy_time %}'
        html += '{{ timestamp|string_to_date }}'
        template = Template(html)
        context = Context({'timestamp': '2014-02-27T17:55:34.2-03:00'})
        timestamp = "Feb. 27, 2014, 5:55 p.m."
        self.assertEqual(timestamp, template.render(context))
