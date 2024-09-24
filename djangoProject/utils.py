from django.apps import apps
import re
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from .models import Insumo
import re


def criar_empresa_e_usuarios(sender, **kwargs):
    if sender.name == 'djangoProject':
        Empresa = apps.get_model('djangoProject', 'Empresa')
        CustomUser = apps.get_model('djangoProject', 'CustomUser')

        # Restante do seu código para criar empresa e usuários
