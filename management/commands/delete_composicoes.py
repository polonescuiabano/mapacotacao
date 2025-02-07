from django.core.management.base import BaseCommand
from mapadecotacao.models import Composicao, Coeficiente, ComposicaoAuxiliar

class Command(BaseCommand):
    help = 'Exclui todas as composições da tabela Composicao'

    def handle(self, *args, **kwargs):
        ComposicaoAuxiliar.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todas as composições foram excluídas com sucesso!'))
