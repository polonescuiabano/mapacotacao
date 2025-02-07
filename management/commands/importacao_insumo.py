import pandas as pd
from datetime import datetime
from mapadecotacao.models import Insumo, Preco
from django.db import transaction

# Caminho do arquivo Excel para os preços Não desonerados
arquivo_excel_nao_desonerado = r'C:\Users\Dell\Documents\Projetos\serpra\NaoDesonerado sinapi\SINAPI_Preco_Ref_Insumos_MT_202411_NaoDesonerado.xlsx'

# Carregar a aba "sheet1" corretamente, pulando as 7 primeiras linhas
df_nao_desonerado = pd.read_excel(arquivo_excel_nao_desonerado, sheet_name='sheet1', skiprows=7)

# Renomear as colunas corretamente, ignorando a coluna D (que será ignorada)
df_nao_desonerado.columns = ['codigo', 'descricao', 'unidade_medida', 'ignorar', 'preco_nao_desonerado']

# Ignorar a coluna 'ignorar' (coluna D)
df_nao_desonerado = df_nao_desonerado[['codigo', 'descricao', 'unidade_medida', 'preco_nao_desonerado']]

# Remover qualquer linha que tenha dados ausentes nas colunas essenciais
insumos_nao_desonerado = df_nao_desonerado.dropna(subset=['codigo', 'descricao', 'unidade_medida', 'preco_nao_desonerado'])

# Substituir os pontos (milhares) por nada, e a vírgula por ponto
insumos_nao_desonerado.loc[:, 'preco_nao_desonerado'] = insumos_nao_desonerado['preco_nao_desonerado'].str.replace('.', '', regex=False)  # Remove os pontos
insumos_nao_desonerado.loc[:, 'preco_nao_desonerado'] = insumos_nao_desonerado['preco_nao_desonerado'].str.replace(',', '.', regex=False)  # Substitui vírgula por ponto

# Converter a coluna 'preco_nao_desonerado' para numérico, tratando erros
insumos_nao_desonerado.loc[:, 'preco_nao_desonerado'] = pd.to_numeric(insumos_nao_desonerado['preco_nao_desonerado'], errors='coerce')

# Data fixa para a cotação: novembro de 2024
data_cotacao = datetime(2024, 11, 1)  # 1 de novembro de 2024

# Usando uma transação para inserir todos os insumos de uma vez
with transaction.atomic():
    for index, row in insumos_nao_desonerado.iterrows():
        try:
            # Verificar se o código do insumo já existe no banco
            insumo_existente = Insumo.objects.filter(codigo=row['codigo']).first()

            if pd.notna(row['preco_nao_desonerado']):
                if insumo_existente:
                    # Se o insumo já existir, cria o preço para o insumo existente
                    Preco.objects.create(
                        insumo=insumo_existente,
                        preco_desonerado=None,  # Caso o preço desonerado seja nulo
                        preco_nao_desonerado=row['preco_nao_desonerado'],
                        cnpj='',  # Insira os valores conforme necessário
                        razao_social='',
                        data_cotacao=data_cotacao,  # Definindo a data para novembro de 2024
                        vendedor='',
                        telefone='',
                        status_preco='Ativo',
                    )
                else:
                    # Caso o insumo não exista, cria o insumo e o preço não desonerado
                    insumo = Insumo(
                        codigo=row['codigo'],
                        nome=row['descricao'],
                        unidade_medida=row['unidade_medida'],
                        tipo='SINAPI',  # Tipo do insumo
                    )
                    insumo.save()

                    # Criar o preço para o insumo com a data de cotação
                    Preco.objects.create(
                        insumo=insumo,
                        preco_desonerado=None,  # Caso o preço desonerado seja nulo
                        preco_nao_desonerado=row['preco_nao_desonerado'],
                        cnpj='',  # Insira os valores conforme necessário
                        razao_social='',
                        data_cotacao=data_cotacao,  # Definindo a data para novembro de 2024
                        vendedor='',
                        telefone='',
                        status_preco='Ativo',
                    )
            else:
                print(f"Valor inválido em 'preco_nao_desonerado' na linha {index + 1}: {row['preco_nao_desonerado']}")
        except Exception as e:
            print(f"Erro na linha {index + 1}: {e}")
