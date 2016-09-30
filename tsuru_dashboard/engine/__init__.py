apps = {}


def register(app):
    apps[app.name] = app


def get(app_name):
    return apps[app_name]
