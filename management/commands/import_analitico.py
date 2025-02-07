import pandas as pd
from datetime import datetime
import os
import django
from decimal import Decimal, ROUND_DOWN
from mapadecotacao.models import Composicao, ComposicaoAuxiliar, Coeficiente


# Função para tratar a conversão dos valores
def convert_to_decimal(value):
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        # Substituir apenas a vírgula por ponto para a conversão
        value = str(value).replace(',', '.')
        print(f"Converting {value} to Decimal...")
        # Converte para Decimal e mantém a precisão necessária
        decimal_value = Decimal(value).quantize(Decimal('0.0001'), rounding=ROUND_DOWN)  # Limitar a 4 casas decimais
        return decimal_value
    except Exception as e:
        print(f"Erro na conversão de valor: {value}, erro: {e}")
        return None


# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mapadecotacao.settings")
django.setup()

# Carregar o arquivo Excel
excel_file = r"C:\Users\Dell\Documents\Projetos\serpra\NaoDesonerado sinapi\SINAPI_Custo_Ref_Composicoes_Analitico_MT_202411_NaoDesonerado.xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=7)  # Começa na linha 8 (header=7 no Python)

# Verificar as primeiras linhas para garantir que o arquivo foi carregado corretamente
print("Primeiras linhas do DataFrame:")
print(df.head())

# Data de cotação fixa (novembro de 2024)
data_cotacao = datetime(2024, 11, 1)

# Loop pelas linhas do DataFrame
for index, row in df.iterrows():
    # Verifica se a linha tem "COMPOSICAO" na coluna L (índice 11)
    if row.iloc[11] == 'COMPOSICAO':
        print(f"Processando linha {index}...")

        # Recupera o código da composição mãe da coluna G (índice 6)
        codigo_composicao_mae = row.iloc[6]
        print(f"Código da composição mãe: {codigo_composicao_mae}")

        try:
            # Buscar a Composicao Mãe no banco de dados pelo código
            composicao_mae = Composicao.objects.get(codigo_composicao=codigo_composicao_mae)
        except Composicao.DoesNotExist:
            print(f"Composição Mãe com código {codigo_composicao_mae} não encontrada. Pulando linha.")
            continue  # Caso não encontre a composição mãe, pula essa linha

        # Criar e salvar a composição auxiliar
        composicao_auxiliar = ComposicaoAuxiliar(
            tipo='SINAPI',
            codigo_composicao_auxiliar=row.iloc[12],  # Coluna M (índice 12)
            descricao_composicao_auxiliar=row.iloc[13],  # Coluna N (índice 13)
            unidade_medida=row.iloc[14],  # Coluna O (índice 14)
            preco_nao_desonerado=convert_to_decimal(row.iloc[17]),  # Coluna R (índice 17) com conversão para decimal
            preco_desonerado=None,  # Caso precise preencher esse campo, coloque aqui
            composicao_mae=composicao_mae,  # Relacionando com a composição mãe
        )
        print(f"Composição Auxiliar: {composicao_auxiliar.codigo_composicao_auxiliar}, Preço não desonerado: {composicao_auxiliar.preco_nao_desonerado}")
        composicao_auxiliar.save()  # Salvar a composição auxiliar

        # Verifica os coeficientes na coluna Q (índice 16)
        coeficientes = row.iloc[16]  # Coluna Q
        print(f"Coeficientes lidos da coluna Q: {coeficientes}")

        if pd.notna(coeficientes):
            # Não separamos mais os coeficientes por vírgula
            coeficiente_values = [coeficientes]  # Mantém o coeficiente como um único valor
            print(f"Coeficientes mantidos como único valor: {coeficiente_values}")
            # Atribuir coeficientes à composição auxiliar e associar com a composição mãe
            for coef in coeficiente_values:
                coef = coef.strip()  # Remove espaços extras
                print(f"Coeficiente processado: {coef}")

                if coef != "":  # Ignorar coeficiente vazio, mas processar o "0"
                    print(f"Coeficiente a ser salvo: {coef}")

                    # Salvar o coeficiente após conversão para decimal
                    coef_decimal = convert_to_decimal(coef)

                    if coef_decimal is not None:
                        coeficiente = Coeficiente(
                            coeficiente=coef_decimal,  # Agora é um valor decimal
                            composicao_auxiliar=composicao_auxiliar,  # Relaciona com a composição auxiliar
                            composicao_mae=composicao_mae  # Relaciona com a composição mãe
                        )
                        coeficiente.save()  # Salvar o coeficiente
                        print(f"Coeficiente {coef_decimal} salvo com sucesso!")

        print(f"Composição Auxiliar {composicao_auxiliar.codigo_composicao_auxiliar} e seus coeficientes foram salvos com sucesso!")

print("Importação concluída!")
