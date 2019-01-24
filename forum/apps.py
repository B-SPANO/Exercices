from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'
    verbose_name = ("Traceability tools - 05 - forum")

    def ready(self):
        from . import signals

