import pandas as pd
import os
import glob
import threading
import time
import matplotlib.pyplot as plt

# Pasta onde estão os arquivos CSV
PASTA_CSV = r"C:\Users\Gabriel Kalebe\Projeto-Final-PCD\Dados\Dados"

# Nomes dos arquivos que vamos criar no final
ARQUIVO_RESUMO = "ResumoMetas.csv"
ARQUIVO_CONSOLIDADO = "Consolidado.csv"
LOCK = threading.Lock()

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

def processar_arquivo(caminho_csv, resultados, dados_consolidados):
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(caminho_csv)
        nome_tribunal = os.path.splitext(os.path.basename(caminho_csv))[0]

        # Calcula as metas para esse tribunal
        meta1 = calcular_meta1(df)
        meta2a = calcular_meta2a(df)
        meta4a = calcular_meta4a(df)

        resultado = {
            'tribunal': nome_tribunal,
            'meta1': meta1,
            'meta2A': meta2a,
            'meta4A': meta4a
        }

        # Protege a escrita nas listas compartilhadas entre threads
        with LOCK:
            resultados.append(resultado)
            dados_consolidados.append(df)

    except Exception as e:
        print(f"Erro no arquivo {caminho_csv}: {e}")

def main():
    # Pega todos os arquivos CSV da pasta
    arquivos_csv = glob.glob(os.path.join(PASTA_CSV, "*.csv"))
    print(f"Encontrei estes arquivos: {arquivos_csv}")

    resultados = []
    dados_consolidados = []
    threads = []

    tempo_inicio = time.time()

    # Cria uma thread para cada arquivo para processar em paralelo
    for caminho in arquivos_csv:
        t = threading.Thread(target=processar_arquivo, args=(caminho, resultados, dados_consolidados))
        t.start()
        threads.append(t)

    # Espera todas as threads terminarem
    for t in threads:
        t.join()

    tempo_fim = time.time()
    duracao = tempo_fim - tempo_inicio
    print(f"Processo paralelo levou {duracao:.2f} segundos")

    # Salva o resumo das metas em um CSV
    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_csv(ARQUIVO_RESUMO, index=False, encoding='utf-8')

    if dados_consolidados:
        df_consolidado = pd.concat(dados_consolidados, ignore_index=True)
        # Salva os dados consolidados em partes para evitar travar
        df_consolidado.to_csv(ARQUIVO_CONSOLIDADO, index=False, encoding='utf-8', chunksize=100000)
    else:
        print("Não encontrei dados para juntar. Confere os arquivos na pasta.")

    # Faz gráfico para cada meta
    for meta in ['meta1', 'meta2A', 'meta4A']:
        df_plot = df_resultado[df_resultado[meta] != 'NA'].copy()
        df_plot[meta] = pd.to_numeric(df_plot[meta])
        df_plot.sort_values(by=meta, ascending=False, inplace=True)

        plt.figure(figsize=(12, 6))
        plt.bar(df_plot['tribunal'], df_plot[meta], color='skyblue')
        plt.xticks(rotation=90)
        plt.ylabel(f'Desempenho {meta} (%)')
        plt.title(f'Cumprimento da {meta.upper()} por Tribunal')
        plt.tight_layout()
        plt.savefig(f"grafico_{meta}.png")
        print(f"Salvei o gráfico {f'grafico_{meta}.png'}")

if __name__ == "__main__":
    main()
