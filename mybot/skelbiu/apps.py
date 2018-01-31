from django.apps import AppConfig


class SkelbiuConfig(AppConfig):
    name = 'skelbiu'

    def ready(self, *args, **kwds):
        from . import signals
