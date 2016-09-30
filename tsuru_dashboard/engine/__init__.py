apps = {}


class AppNotFound(Exception):
    pass


class ObjectIsNotApp(Exception):
    pass


class App(object):
    tabs = {}

    def register_tab(self, tab):
        self.tabs[tab.name] = tab

    def get_tab(self, tab_name):
        return self.tabs[tab_name]


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
