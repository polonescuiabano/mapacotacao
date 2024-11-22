from django.apps import AppConfig


class MapadecotacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mapadecotacao'

    def ready(self):
        import mapadecotacao.signals
