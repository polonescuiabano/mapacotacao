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

# Carregar o arquivo Excel
excel_file = r"C:\Users\Dell\Documents\Projetos\serpra\NaoDesonerado sinapi\SINAPI_Custo_Ref_Composicoes_Sintetico_MT_202411_NaoDesonerado.xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=5)  # Começa na linha 7 (header=6 no Python)

# Verificar as primeiras linhas para garantir que o arquivo foi carregado corretamente
print(df.head())

# Data de cotação fixa (novembro de 2024)
data_cotacao = datetime(2024, 11, 1)

# Loop pelas linhas do DataFrame
for index, row in df.iterrows():
    # Recuperar os valores das colunas
    codigo_composicao = row.iloc[6]  # A coluna 'G' (índice 6)
    descricao_composicao = row.iloc[7]  # A coluna 'H' (índice 7)
    unidade_medida = row.iloc[8]  # A coluna 'I' (índice 8)
    preco_nao_desonerado = row.iloc[10]  # A coluna 'K' (índice 10)

    # Converter o preço para o formato decimal
    preco_nao_desonerado = convert_to_decimal(preco_nao_desonerado)

    # Verifica se a linha possui dados válidos
    if pd.notna(codigo_composicao) and pd.notna(descricao_composicao) and preco_nao_desonerado is not None:
        # Criar e salvar a composição
        composicao = Composicao(
            tipo='SINAPI',  # Tipo da tabela
            descricao_classe=row.iloc[0],  # Coluna A
            sigla_classe=row.iloc[1],  # Coluna B
            codigo_composicao=codigo_composicao,
            descricao_composicao=descricao_composicao,
            unidade_medida=unidade_medida,
            preco_nao_desonerado=preco_nao_desonerado,  # Preço não desonerado convertido
            data_cotacao=data_cotacao
        )
        composicao.save()  # Salvar a composição

print("Importação concluída!")
