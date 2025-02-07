import pandas as pd
from datetime import datetime
import os
import django
from mapadecotacao.models import Composicao, Insumo
import decimal

# Função para tratar a conversão dos valores
def convert_to_decimal(value):
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        return decimal.Decimal(str(value).replace('.', '').replace(',', '.'))
    except decimal.InvalidOperation:
        return None

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapadecotacao.settings")
django.setup()

# Carregar o arquivo Excel
excel_file = r"C:\Users\Dell\Documents\Projetos\serpra\NaoDesonerado sinapi\SINAPI_Custo_Ref_Composicoes_Analitico_MT_202411_NaoDesonerado.xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=7)

# Verificar os nomes das colunas
print(df.columns)

# Data de cotação fixa (novembro de 2024)
data_cotacao = datetime(2024, 11, 1)

# Inicializar a variável para armazenar os dados de composição
composicao_atual = None
codigo_composicao_anterior = None

# Função para buscar um insumo existente no banco de dados
def buscar_insumo_existente(codigo_item):
    try:
        return Insumo.objects.get(codigo=codigo_item)  # Alterado para usar 'codigo' no lugar de 'codigo_item'
    except Insumo.DoesNotExist:
        return None

# Função para verificar se a composição mãe já existe
def verificar_composicao_existente(codigo_composicao):
    try:
        return Composicao.objects.get(codigo_composicao=codigo_composicao)
    except Composicao.DoesNotExist:
        return None

# Loop pelas linhas do DataFrame
for index, row in df.iterrows():
    # Recuperar o código da composição (usando o índice correto para a coluna G)
    codigo_composicao = row.iloc[6]  # A coluna 'G' (índice 6)

    # Se o código da composição mudar ou for o início de uma nova composição mãe
    if pd.notna(codigo_composicao) and (codigo_composicao != codigo_composicao_anterior):
        # Se já existia uma composição anterior, salvamos os dados
        if composicao_atual:
            composicao_atual.save()  # Salvar a composição anterior

        # Verifica se a composição mãe já existe
        composicao_existente = verificar_composicao_existente(codigo_composicao)

        if composicao_existente:
            # Se a composição mãe já existe, utilizamos a composição existente
            composicao_atual = composicao_existente
        else:
            # Caso contrário, criamos uma nova composição mãe
            composicao_atual = Composicao(
                tipo='SINAPI',  # Tipo da tabela
                descricao_classe=row.iloc[0],  # Coluna A
                sigla_classe=row.iloc[1],  # Coluna B
                codigo_composicao=codigo_composicao,
                descricao_composicao=row.iloc[7],  # Coluna H
                unidade_medida=row.iloc[8],  # Coluna I
                custo_total=convert_to_decimal(row.iloc[10]),  # Coluna K (Custo total) com conversão
                tipo_item=row.iloc[11],  # Coluna L (Tipo de item)
                codigo_item=row.iloc[12],  # Coluna M (Código de item)
                descricao_item=row.iloc[13],  # Coluna N
                unidade_item=row.iloc[14],  # Coluna O
                coeficiente=convert_to_decimal(row.iloc[16]),  # Coluna Q
                preco_unitario=convert_to_decimal(row.iloc[17]),  # Coluna R
                custo_total_item=convert_to_decimal(row.iloc[18]),  # Coluna S
                custo_mao_obra=None,  # Inicializa como None (não atribui valor ainda)
                percent_mao_obra=convert_to_decimal(row.iloc[20]),  # Coluna U
                custo_material=convert_to_decimal(row.iloc[21]),  # Coluna V
                percent_material=convert_to_decimal(row.iloc[22]),  # Coluna W
                custo_equipamento=convert_to_decimal(row.iloc[23]),  # Coluna X
                percent_equipamento=convert_to_decimal(row.iloc[24]),  # Coluna Y
                custo_servicos_terceiros=convert_to_decimal(row.iloc[25]),  # Coluna Z
                percent_servicos_terceiros=convert_to_decimal(row.iloc[26]),  # Coluna AA
                custo_outros=convert_to_decimal(row.iloc[27]),  # Coluna AB
                percent_outros=convert_to_decimal(row.iloc[28]),  # Coluna AC
                data_cotacao=data_cotacao
            )

            # Agora, salva a composição principal criada
            composicao_atual.save()

        # Atualizar o código da composição anterior
        codigo_composicao_anterior = codigo_composicao

    # Verifica o tipo de item (composto ou insumo)
    tipo_item = row.iloc[11]  # Coluna L

    # Se for uma composição auxiliar
    if tipo_item == 'COMPOSICAO':
        # Ignora a composição auxiliar e não salva no banco
        print(f"Composição auxiliar encontrada com código {row.iloc[12]}, ignorando inserção.")

    # Se for um insumo
    elif tipo_item == 'INSUMO':
        insumo_existente = buscar_insumo_existente(row.iloc[12])  # Coluna M (Código do insumo)

        if insumo_existente:
            # Relacionar o insumo existente à composição mãe
            composicao_atual.insumos.add(insumo_existente)
        else:
            # Criar um novo insumo caso não exista
            composicao_insumo = Insumo(
                tipo='SINAPI',  # Tipo da tabela
                descricao_classe=row.iloc[0],  # Coluna A
                sigla_classe=row.iloc[1],  # Coluna B
                codigo=row.iloc[12],  # Coluna M (Código do insumo)
                nome=row.iloc[13],  # Coluna N (Nome do insumo)
                unidade_medida=row.iloc[14],  # Coluna O
            )
            composicao_insumo.save()
            composicao_atual.insumos.add(composicao_insumo)  # Relaciona o insumo à composição mãe

# Ao final, salvamos a última composição (caso não tenha sido salva no loop)
if composicao_atual:
    composicao_atual.save()

print("Importação concluída!")
