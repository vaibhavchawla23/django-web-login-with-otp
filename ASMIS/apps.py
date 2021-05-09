from django.apps import AppConfig


class AsmisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ASMIS'

    def ready(self):
        import ASMIS.signals
