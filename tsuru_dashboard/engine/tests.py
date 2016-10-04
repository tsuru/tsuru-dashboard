from django.test import TestCase

from . import register, get, unregister, AppNotFound, App, TabNotFound


class RegisterTest(TestCase):
    def test_register(self):
        class MyApp(App):
            name = 'myapp'

        register(MyApp)
        my_app = get('myapp')

        self.assertIsInstance(my_app, MyApp)

    def test_unregister(self):
        class MyApp(App):
            name = 'myapp'

        register(MyApp)
        unregister('myapp')

        with self.assertRaises(AppNotFound):
            get('myapp')


class AppTest(TestCase):
    def test_register_tab(self):
        class MyTab(object):
            name = 'mytab'

        class MyApp(App):
            name = 'myapp'

        my_app = MyApp()
        my_app.register_tab(MyTab)
        my_tab = my_app.get_tab('mytab')

        self.assertEqual(my_tab, MyTab)

    def test_unregister_tab(self):
        class MyTab(object):
            name = 'mytab'

        class MyApp(App):
            name = 'myapp'

        my_app = MyApp()
        my_app.register_tab(MyTab)

        my_app.unregister_tab('mytab')

        with self.assertRaises(TabNotFound):
            my_app.get_tab('mytab')
