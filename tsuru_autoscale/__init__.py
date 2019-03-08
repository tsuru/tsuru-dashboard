from tsuru_dashboard import engine
from tsuru_autoscale import settings

class AutoScaleTab(engine.Tab):
    name = 'autoscale'
    url_name = 'autoscale-app-info'

if settings.AUTOSCALE_HOST:
    try:
        engine.get('app').register_tab(AutoScaleTab)
    except engine.AppNotFound:
        pass
