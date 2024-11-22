from django.utils.dateparse import parse_date
from django import forms
from .models import Insumo
from .models import CustomUser


class OrcamentoForm(forms.Form):
    # Campos para informações da empresa
    nome_empresa = forms.CharField(label='Nome da Empresa', max_length=100)
    cnpj = forms.CharField(label='CNPJ', max_length=18)
    telefone = forms.CharField(label='Telefone', max_length=20)
    email = forms.EmailField(label='E-mail', max_length=100)

    # Campos para informações do insumo
    codigo_insumo = forms.CharField(label='Código do Insumo', max_length=100)
    nome_insumo = forms.CharField(label='Nome do Insumo', max_length=100)
    unidade_medida = forms.CharField(label='Unidade de Medida', max_length=50)
    preco = forms.DecimalField(label='Preço do Insumo', max_digits=10, decimal_places=2)
    razao_social = forms.CharField(label='Razão Social', max_length=100, required=False)
    data_cotacao = forms.DateField(label='Data de Cotação', widget=forms.DateInput(attrs={'type': 'date'}),
                                   required=False)
    vendedor = forms.CharField(label='Vendedor', max_length=100, required=False)
    telefone_vendedor = forms.CharField(label='Telefone do Vendedor', max_length=20, required=False)
    status_preco = forms.CharField(label='Status do Preço', max_length=100, required=False)
    documento = forms.FileField(label='Documento (PDF)')


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ConsultaInsumoForm(forms.Form):
    nome_insumo = forms.CharField(label='Nome do Insumo', max_length=100)
    uf = forms.CharField(label='UF', max_length=2)


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['codigo', 'nome', 'unidade_medida']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
            instance.empresa = user.empresa
        if commit:
            instance.save()
        return instance

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo']