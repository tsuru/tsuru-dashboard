from tsuru_dashboard import engine


class ResourcesTab(engine.Tab):
    name = 'resources'
    url_name = 'app-resources'


class InfoTab(engine.Tab):
    name = 'info'
    url_name = 'app-info'


class DeploysTab(engine.Tab):
    name = 'deploys'
    url_name = 'app-deploys'


class EventsTab(engine.Tab):
    name = 'events'
    url_name = 'app-events'


class LogTab(engine.Tab):
    name = 'log'
    url_name = 'app-log'


class SettingsTab(engine.Tab):
    name = 'settings'
    url_name = 'app-settings'


class App(engine.App):
    name = 'app'

    def __init__(self):
        self.tabs = [ResourcesTab, InfoTab, DeploysTab, EventsTab, LogTab, SettingsTab]


engine.register(App)
