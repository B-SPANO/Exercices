from django.apps import AppConfig


class ForumConfig(AppConfig):
    """ Configuration class """
    name = 'forum'
    verbose_name = ("Traceability tools - 05 - forum")

    def ready(self):
        from . import signals
