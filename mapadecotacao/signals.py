from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Empresa


@receiver(post_migrate)
def create_empresa(sender, **kwargs):
    if sender.name == 'mapadecotacao':
        # Verifica se a empresa já existe para evitar duplicatas
        if not Empresa.objects.filter(nome='Proconsult').exists():
            Empresa.objects.create(nome='Proconsult')
