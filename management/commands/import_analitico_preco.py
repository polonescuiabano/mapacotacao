import pandas as pd
from datetime import datetime
import decimal
import os
import django
from mapadecotacao.models import ComposicaoAuxiliar


# Função para tratar a conversão dos valores
def convert_to_decimal(value):
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        # Remover pontos (caso existam como separador de milhar) e substituir vírgula por ponto
        value = str(value).replace('.', '').replace(',', '.')
        return decimal.Decimal(value)
    except decimal.InvalidOperation:
        return None


# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapadecotacao.settings")
django.setup()

# Carregar o arquivo Excel
excel_file = r"C:\Users\Dell\Documents\Projetos\serpra\desonerado sinapi\SINAPI_Custo_Ref_Composicoes_Analitico_MT_202411_Desonerado.xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=7)  # Começa na linha 8 (header=7 no Python)

# Verificar as primeiras linhas para garantir que o arquivo foi carregado corretamente
print(df.head())

# Inicializa o contador para percorrer as composições auxiliares
composicao_auxiliar_index = 0

# Loop pelas linhas do DataFrame
for index, row in df.iterrows():
    # Verificar se a linha corresponde a uma composição (Coluna L com valor "COMPOSICAO")
    if row.iloc[11] == 'COMPOSICAO':  # Coluna L (índice 11)
        print(f"Processando linha {index}...")

        preco_desonerado = convert_to_decimal(row.iloc[17])  # Coluna R (índice 17)

        if preco_desonerado is not None:
            # Buscar a composição auxiliar pela ordem do índice
            try:
                composicao_auxiliar = ComposicaoAuxiliar.objects.all()[composicao_auxiliar_index]

                # Atualizar o preço desonerado na composição auxiliar
                composicao_auxiliar.preco_desonerado = preco_desonerado
                composicao_auxiliar.save()

                print(
                    f"Preço desonerado para a composição auxiliar {composicao_auxiliar.codigo_composicao_auxiliar} atualizado com sucesso!")

                # Incrementar o índice para a próxima composição auxiliar
                composicao_auxiliar_index += 1

            except IndexError:
                print(f"Composição auxiliar com índice {composicao_auxiliar_index} não encontrada. Pulando linha.")
            except Exception as e:
                print(f"Erro ao atualizar a composição auxiliar: {e}")
        else:
            print(f"Preço desonerado inválido para a linha {index}. Pulando linha.")

print("Importação e atualização concluída!")
