from django.test import TestCase

from . import register, get


class RegisterTest(TestCase):
    def test_register(self):
        class MyApp(object):
            name = 'myapp'
        register(MyApp)
        my_app = get('myapp')

        self.assertEqual(my_app, MyApp)
