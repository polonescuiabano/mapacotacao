import pandas as pd
from datetime import datetime
import decimal
import os
import django
from mapadecotacao.models import Composicao

# Função para tratar a conversão dos valores
def convert_to_decimal(value):
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        # Remove o ponto e substitui a vírgula por ponto
        return decimal.Decimal(str(value).replace('.', '').replace(',', '.'))
    except decimal.InvalidOperation:
        return None

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapadecotacao.settings")
django.setup()

# Carregar o arquivo Excel com os dados de "Desonerado"
excel_file = r"C:\Users\Dell\Documents\Projetos\serpra\desonerado sinapi\SINAPI_Custo_Ref_Composicoes_Sintetico_MT_202411_Desonerado.xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=5)  # Começa na linha 7 (header=6 no Python)

# Verificar as primeiras linhas para garantir que o arquivo foi carregado corretamente
print(df.head())

# Data de cotação fixa (novembro de 2024)
data_cotacao = datetime(2024, 11, 1)

# Inicializa o contador para percorrer as composições
composicao_index = 0

# Loop pelas linhas do DataFrame
for index, row in df.iterrows():
    # Verifica se a linha contém a composição a ser atualizada
    if pd.notna(row.iloc[6]):  # Coluna G (índice 6) não pode ser NaN
        print(f"Processando linha {index}...")

        # Recupera os dados da linha
        codigo_composicao = row.iloc[6]  # A coluna 'G' (índice 6)
        preco_desonerado = convert_to_decimal(row.iloc[10])  # A coluna 'K' (índice 10)

        if preco_desonerado is not None:
            try:
                # Buscar a composição pela ordem de chegada
                composicao = Composicao.objects.all()[composicao_index]

                # Atualizar o preço desonerado na composição
                composicao.preco_desonerado = preco_desonerado
                composicao.save()

                print(
                    f"Preço desonerado para a composição {composicao.codigo_composicao} atualizado com sucesso!")

                # Incrementar o índice para a próxima composição
                composicao_index += 1

            except IndexError:
                print(f"Composição com índice {composicao_index} não encontrada. Pulando linha.")
            except Exception as e:
                print(f"Erro ao atualizar a composição: {e}")
        else:
            print(f"Preço desonerado inválido para a linha {index}. Pulando linha.")

print("Importação e atualização concluída!")
