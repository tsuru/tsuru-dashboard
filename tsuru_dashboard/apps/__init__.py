from tsuru_dashboard import engine


class App(engine.App):
    name = 'app'


engine.register(App)
