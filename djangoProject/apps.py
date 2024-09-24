from django.apps import AppConfig


class DjangoProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoProject'

    def ready(self):
        import djangoProject.signals
