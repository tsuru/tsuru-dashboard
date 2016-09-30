from django.test import TestCase

from . import register, get, unregister, AppNotFound, App


class RegisterTest(TestCase):
    def test_register(self):
        class MyApp(App):
            name = 'myapp'

        register(MyApp)
        my_app = get('myapp')

        self.assertEqual(my_app, MyApp)

    def test_unregister(self):
        class MyApp(App):
            name = 'myapp'

        register(MyApp)
        unregister('myapp')

        with self.assertRaises(AppNotFound):
            get('myapp')
