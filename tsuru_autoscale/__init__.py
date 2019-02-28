from tsuru_dashboard import engine


class AutoScaleTab(engine.Tab):
    name = 'autoscale'
    url_name = 'autoscale-app-info'

try:
    engine.get('app').register_tab(AutoScaleTab)
except engine.AppNotFound:
    pass
