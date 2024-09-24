from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission as DjangoPermission
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Empresa(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class ContatoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome_vendedor = models.CharField(max_length=100)
    telefone_vendedor = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.empresa.nome} - {self.nome_vendedor}"

class CustomUser(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

class CustomUserGroup(models.Model):
    custom_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class CustomUserPermission(models.Model):
    custom_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(DjangoPermission, on_delete=models.CASCADE)

CustomUser = get_user_model()

class Preco(models.Model):
    insumo = models.ForeignKey('Insumo', on_delete=models.CASCADE, related_name='precos')
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cnpj = models.CharField(max_length=20)
    razao_social = models.CharField(max_length=100)
    data_cotacao = models.DateField(null=True, blank=True)
    vendedor = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    status_preco = models.CharField(max_length=20, blank=True, null=True)

class Insumo(models.Model):
    codigo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100, blank=False)
    unidade_medida = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)


    def __str__(self):
        return self.nome

    def atualizar_preco(self, preco, cnpj, razao_social, data_cotacao, vendedor, telefone, status_preco):
        # Verifica se já existe um preço para esse insumo nesta data de cotação
        preco_existente = self.precos.filter(data_cotacao=data_cotacao).first()
        if preco_existente:
            preco_existente.preco = preco
            preco_existente.cnpj = cnpj
            preco_existente.razao_social = razao_social
            preco_existente.vendedor = vendedor
            preco_existente.telefone = telefone
            preco_existente.status_preco = status_preco
            preco_existente.save()
        else:
            preco_obj = Preco.objects.create(
                insumo=self,
                preco=preco,
                cnpj=cnpj,
                razao_social=razao_social,
                data_cotacao=data_cotacao,
                vendedor=vendedor,
                telefone=telefone,
                status_preco=status_preco
            )

class ArquivoAnexado(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='arquivos_anexados/')
    preco = models.ForeignKey(Preco, on_delete=models.CASCADE, related_name='arquivos_anexados')


    def __str__(self):
        return f"Arquivo Anexado para {self.empresa.nome}"

class Mapa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Certifique-se de importar o modelo Empresa
    arquivo = models.FileField(upload_to='mapas/')  # O campo arquivo para armazenar o relatório
    title = models.CharField(max_length=100)  # Adicionando um campo de título
    # Outros campos e métodos conforme necessário

    def __str__(self):
        return f"Mapa de {self.usuario.username} para {self.empresa.nome}"



class AvaliacaoInsumo(models.Model):
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    insumo = models.ForeignKey('Insumo', on_delete=models.CASCADE)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.avaliador} - {self.insumo} - Aprovado: {self.aprovado}"
