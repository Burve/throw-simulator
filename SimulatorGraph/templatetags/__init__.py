from django.apps import AppConfig


class YourAppConfig(AppConfig):
    name = 'SimulatorGraph'

    def ready(self):
        import SimulatorGraph.templatetags.bootstrap_filters
