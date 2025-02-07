import pandas as pd
import os
import django
from mapadecotacao.models import Insumo, Coeficiente, Composicao
import decimal

# Função para tratar a conversão dos valores
def convert_to_decimal(value):
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        # Converte o valor da coluna Q para decimal, substituindo vírgula por ponto
        return decimal.Decimal(str(value).replace(',', '.'))
    except decimal.InvalidOperation:
        return None

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapadecotacao.settings")
django.setup()

# Carregar o arquivo Excel com os dados de "NaoDesonerado"
excel_file = r"C:\Users\Dell\Documents\Projetos\serpra\NaoDesonerado sinapi\SINAPI_Custo_Ref_Composicoes_Analitico_MT_202411_NaoDesonerado.xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=7)  # Começa na linha 8 (header=7 no Python)

# Verificar as primeiras linhas para garantir que o arquivo foi carregado corretamente
print(df.head())

# Função para tratar o código, removendo o sufixo .0 quando necessário
def format_codigo(codigo):
    # Verifica se o código tem a forma decimal com ".0" e converte para string sem o ".0"
    codigo_str = str(codigo).strip()
    if codigo_str.endswith('.0'):
        return str(int(float(codigo_str)))  # Converte para inteiro e depois de volta para string
    return codigo_str

# Loop pelas linhas do DataFrame
for index, row in df.iterrows():
    # Verifica se a coluna "L" corresponde a "INSUMO"
    if row.iloc[11] == "INSUMO":  # Coluna "L" (índice 11)
        print(f"Processando linha {index}...")

        # Recupera o código do insumo (coluna "M" - índice 12) e formata
        codigo = format_codigo(row.iloc[12])  # Formata o código para string sem ".0"

        # Recupera o coeficiente da coluna "Q" (índice 16) e converte para decimal
        coeficiente_str = row.iloc[16]  # Coluna "Q" (índice 16)
        coeficiente_decimal = convert_to_decimal(coeficiente_str)

        if coeficiente_decimal is None:
            print(f"Coeficiente '{coeficiente_str}' não é um valor válido. Pulando linha.")
            continue

        # Recupera o código da composição mãe (coluna "G" - índice 6)
        codigo_composicao_mae = row.iloc[6]  # Coluna "G" (índice 6)

        try:
            # Buscar o insumo no banco de dados com o código do insumo (agora como string)
            insumo = Insumo.objects.get(codigo=codigo)  # Procurar pelo 'codigo' que é CharField

            # Buscar a composição mãe no banco de dados com o código da composição mãe
            composicao_mae = Composicao.objects.get(codigo_composicao=codigo_composicao_mae)

            # Criar o coeficiente e associá-lo ao insumo e à composição mãe
            coeficiente = Coeficiente(
                coeficiente=coeficiente_decimal,  # Valor do coeficiente convertido
                insumo=insumo,  # Relaciona com o insumo
                composicao_mae=composicao_mae  # Relaciona com a composição mãe
            )
            coeficiente.save()

            print(f"Coeficiente {coeficiente_decimal} associado ao insumo {codigo} e à composição mãe {codigo_composicao_mae} salvo com sucesso!")

        except Insumo.DoesNotExist:
            print(f"Insumo com código {codigo} não encontrado. Pulando linha.")
        except Composicao.DoesNotExist:
            print(f"Composição Mãe com código {codigo_composicao_mae} não encontrada. Pulando linha.")
        except Exception as e:
            print(f"Erro ao adicionar coeficiente: {e}")

print("Importação concluída!")
