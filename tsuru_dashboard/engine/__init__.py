apps = {}


class AppNotFound(Exception):
    pass


class ObjectIsNotApp(Exception):
    pass


class App(object):
    pass


def register(app):
    if not issubclass(app, App):
        raise ObjectIsNotApp

    apps[app.name] = app


def get(app_name):
    if app_name not in apps:
        raise AppNotFound

    return apps[app_name]


def unregister(app_name):
    del apps[app_name]
