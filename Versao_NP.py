import pandas as pd
import os
import glob
import time
import matplotlib.pyplot as plt

# Pasta onde estão os arquivos CSV
PASTA_CSV = r"C:\Users\Gabriel Kalebe\Projeto-Final-PCD\Dados\Dados"

# Nomes dos arquivos que vamos criar no final
ARQUIVO_RESUMO = "ResumoMetas_NP.csv"
ARQUIVO_CONSOLIDADO = "Consolidado_NP.csv"

def calcular_meta1(df):
    try:
        julgados = df['julgados_2025'].sum()
        novos = df['casos_novos_2025'].sum()
        des = df['dessobrestados_2025'].sum()
        sus = df['suspensos_2025'].sum()
        denom = novos + des - sus
        return round((julgados / denom) * 100, 2) if denom != 0 else 'NA'
    except KeyError:
        return 'NA'

def calcular_meta2a(df):
    try:
        julgados = df['julgados_1grau_2025'].sum()
        distribuidos = df['distribuidos_1grau_2025'].sum()
        suspensos = df['suspensos_1grau_2025'].sum()
        denom = distribuidos - suspensos
        return round((julgados / denom) * (1000 / 8), 2) if denom != 0 else 'NA'
    except KeyError:
        return 'NA'

def calcular_meta4a(df):
    try:
        julgados = df['julgados_acao_admin_2025'].sum()
        distribuidos = df['distribuidos_acao_admin_2025'].sum()
        suspensos = df['suspensos_acao_admin_2025'].sum()
        denom = distribuidos - suspensos
        return round((julgados / denom) * (1000 / 6.5), 2) if denom != 0 else 'NA'
    except KeyError:
        return 'NA'

def main():
    # Pega todos os arquivos CSV da pasta
    arquivos_csv = glob.glob(os.path.join(PASTA_CSV, "*.csv"))
    print(f"Encontrei esses arquivos: {arquivos_csv}")

    resultados = []
    dados_consolidados = []

    tempo_inicio = time.time()

    # Processa um arquivo por vez, na sequência
    for caminho_csv in arquivos_csv:
        try:
            df = pd.read_csv(caminho_csv)
            nome_tribunal = os.path.splitext(os.path.basename(caminho_csv))[0]

            meta1 = calcular_meta1(df)
            meta2a = calcular_meta2a(df)
            meta4a = calcular_meta4a(df)

            resultados.append({
                'tribunal': nome_tribunal,
                'meta1': meta1,
                'meta2A': meta2a,
                'meta4A': meta4a
            })

            dados_consolidados.append(df)
        except Exception as e:
            print(f"Erro no arquivo {caminho_csv}: {e}")

    tempo_fim = time.time()
    duracao = tempo_fim - tempo_inicio
    print(f"Rodou tudo em sequência em {duracao:.2f} segundos")

    # Salva o resumo das metas
    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_csv(ARQUIVO_RESUMO, index=False, encoding='utf-8')

    if dados_consolidados:
        df_consolidado = pd.concat(dados_consolidados, ignore_index=True)
        # Salva os dados consolidados em pedaços para não travar
        df_consolidado.to_csv(ARQUIVO_CONSOLIDADO, index=False, encoding='utf-8', chunksize=100000)
    else:
        print("Não achei dados para juntar. Confere os arquivos na pasta.")

    return duracao

if __name__ == "__main__":
    main()
