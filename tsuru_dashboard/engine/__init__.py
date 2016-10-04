apps = {}


class AppNotFound(Exception):
    pass


class ObjectIsNotApp(Exception):
    pass


class TabNotFound(Exception):
    pass


class Tab(object):
    pass


class App(object):
    def __init__(self):
        self.tabs = []

    def register_tab(self, tab):
        self.tabs.append(tab)

    def get_tab(self, tab_name):
        for tab in self.tabs:
            if tab_name == tab.name:
                return tab

        raise TabNotFound

    def unregister_tab(self, tab_name):
        tab = self.get_tab(tab_name)
        self.tabs.remove(tab)


def register(app):
    if not issubclass(app, App):
        raise ObjectIsNotApp

    apps[app.name] = app()


def get(app_name):
    if app_name not in apps:
        raise AppNotFound

    return apps[app_name]


def unregister(app_name):
    del apps[app_name]
