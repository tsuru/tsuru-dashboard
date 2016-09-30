apps = {}


class AppNotFound(Exception):
    pass


def register(app):
    apps[app.name] = app


def get(app_name):
    if app_name not in apps:
        raise AppNotFound

    return apps[app_name]


def unregister(app_name):
    del apps[app_name]
