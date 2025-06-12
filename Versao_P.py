import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
from numba import jit
import dask.dataframe as dd

#---------------------------------------------------------------- Calculo de Metas --------------------------------------------------------------------------------------

@jit(nopython=True)
def calcular_meta_numba(numerador, denominador, multiplicador):
    """
    Calcula metas de forma otimizada usando Numba.
    Evita divisão por zero e NaN. Garante tipo float64 para resultados.
    """
    resultado = np.empty_like(numerador, dtype=np.float64)
    for i in range(len(numerador)):
        if denominador[i] == 0 or np.isnan(numerador[i]) or np.isnan(denominador[i]):
            resultado[i] = np.nan
        else:
            resultado[i] = round((numerador[i] / denominador[i]) * multiplicador, 2)
    return resultado

def calcula_meta_segura(df_slice, num_col, den_cols, multiplicador):
    """
    Prepara os dados e chama a função Numba para calcular a meta para um slice do DataFrame.
    Trata colunas ausentes e NaN de forma robusta e otimizada.
    """
    # Lista de nomes de colunas do denominador (removendo prefixo '-')
    den_cols_cleaned = [col.lstrip('-') for col in den_cols]
    colunas_necessarias = [num_col] + den_cols_cleaned

    # Verifica se todas as colunas necessárias estão presentes no slice
    if not all(col in df_slice.columns for col in colunas_necessarias):
        return np.full(len(df_slice), np.nan)
    
    numerador = df_slice[num_col].fillna(0).values.astype(np.float64)
    denominador = np.zeros_like(numerador, dtype=np.float64)
    
    for col in den_cols:
        col_name = col.lstrip('-')
        col_values = df_slice[col_name].fillna(0).values.astype(np.float64)
        if col.startswith('-'):
            denominador -= col_values
        else:
            denominador += col_values
    
    return calcular_meta_numba(numerador, denominador, multiplicador)

# Dicionário que mapeia nomes das metas para funções que calculam cada uma
METAS = {
    "meta1": lambda df: calcula_meta_segura(df, "julgados_2025", ["casos_novos_2025", "dessobrestados_2025", "-suspensos_2025"], 100),
    "meta2A": lambda df: calcula_meta_segura(df, "julgm2_a", ["distm2_a", "-suspm2_a"], 125),
    "meta2B": lambda df: calcula_meta_segura(df, "julgm2_b", ["distm2_b", "-suspm2_b"], 111.11),
    "meta2C": lambda df: calcula_meta_segura(df, "julgm2_c", ["distm2_c", "-suspm2_c"], 105.26),
    "meta2ANT": lambda df: calcula_meta_segura(df, "julgm2_ant", ["distm2_ant", "-suspm2_ant"], 100),
    "meta4A": lambda df: calcula_meta_segura(df, "julgm4_a", ["distm4_a", "-suspm4_a"], 153.85),
    "meta4B": lambda df: calcula_meta_segura(df, "julgm4_b", ["distm4_b", "-suspm4_b"], 100),
    "meta6": lambda df: calcula_meta_segura(df, "julgm6_a", ["distm6_a", "-suspm6_a"], 100),
    "meta7A": lambda df: calcula_meta_segura(df, "julgm7_a", ["distm7_a", "-suspm7_a"], 200),
    "meta7B": lambda df: calcula_meta_segura(df, "julgm7_b", ["distm7_b", "-suspm7_b"], 200),
    "meta8A": lambda df: calcula_meta_segura(df, "julgm8_a", ["distm8_a", "-suspm8_a"], 133.33),
    "meta8B": lambda df: calcula_meta_segura(df, "julgm8_b", ["distm8_b", "-suspm8_b"], 111.11),
    "meta10A": lambda df: calcula_meta_segura(df, "julgm10_a", ["distm10_a", "-suspm10_a"], 111.11),
    "meta10B": lambda df: calcula_meta_segura(df, "julgm10_b", ["distm10_b", "-suspm10_b"], 100),
}

#-------------------------------------------------------- Gera gráficos de barras --------------------------------------------------------------------------------

def gerar_graficos(df):
    """
    Gera e salva gráficos de desempenho para cada tribunal.
    """
    print("Iniciando geração de gráficos por tribunal...")
    sns.set(style="whitegrid")
    os.makedirs("GraficosPorTribunal", exist_ok=True)

    for _, row in df.iterrows():
        tribunal = row["tribunal"]
        metas_presentes = [meta for meta in METAS.keys() if meta in row and pd.notna(row[meta])]
        
        if not metas_presentes: 
            continue

        valores = row[metas_presentes]
        cores = ['green' if v >= 100 else 'red' for v in valores]

        plt.figure(figsize=(12, 6))
        plt.bar(metas_presentes, valores, color=cores)
        plt.axhline(100, color='gray', linestyle='--', linewidth=1)

        for i, v in enumerate(valores):
            label = f"{v:.2f}"
            plt.text(i, v + 1, label, ha='center', va='bottom', fontsize=9)

        plt.title(f"Desempenho nas Metas - {tribunal}")
        plt.ylabel("% de Cumprimento")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"GraficosPorTribunal/grafico_{tribunal}.png")
        plt.close()
    print("Gráficos por tribunal gerados na pasta 'GraficosPorTribunal'.")

# --- Função para gerar gráfico consolidado ---
def gerar_grafico_consolidado(df_resultado):
    """
    Gera um gráfico de barras consolidado mostrando a média de cumprimento de cada meta
    para todos os tribunais.
    """
    print("Gerando gráfico consolidado de metas...")
    sns.set(style="whitegrid")
    os.makedirs("GraficosConsolidados", exist_ok=True)

    df_medias = df_resultado[list(METAS.keys())].mean().reset_index()
    df_medias.columns = ['meta', 'valor_medio']

    if df_medias.empty:
        print("Nenhum dado de meta válido para gerar o gráfico consolidado.")
        return

    cores = ['green' if v >= 100 else 'red' for v in df_medias['valor_medio']]

    plt.figure(figsize=(14, 7))
    plt.bar(df_medias['meta'], df_medias['valor_medio'], color=cores)
    plt.axhline(100, color='gray', linestyle='--', linewidth=1, label='Meta Ideal (100%)')

    for i, v in enumerate(df_medias['valor_medio']):
        label = f"{v:.2f}"
        plt.text(i, v + 1, label, ha='center', va='bottom', fontsize=10)

    plt.title("Desempenho Médio das Metas (Todos os Tribunais)")
    plt.ylabel("% de Cumprimento Médio")
    plt.xticks(rotation=45, ha='right')
    plt.ylim(bottom=0) 
    plt.legend()
    plt.tight_layout()
    plt.savefig("GraficosConsolidados/grafico_consolidado_metas.png")
    plt.close()
    print("Gráfico consolidado 'grafico_consolidado_metas.png' gerado na pasta 'GraficosConsolidados'.")


# -------------------------------------------------------------- Função principal do programa ------------------------------------------------------------------------

def main():
    inicio = time.time()
    caminho_csv = input("Informe o caminho completo para 'todos_csvs.csv': ").strip().replace('"', '')
    
    print("Iniciando processamento com Dask...")

    try:
        # DEFINIÇÃO EXPLÍCITA DOS DTYPES: Crucial para evitar erros de inferência e otimizar.
        dtypes_explicit = {
            'sigla_tribunal': str,
            'julgados_2025': float, 'casos_novos_2025': float, 'dessobrestados_2025': float, 'suspensos_2025': float,
            'julgm2_a': float, 'distm2_a': float, 'suspm2_a': float,
            'julgm2_b': float, 'distm2_b': float, 'suspm2_b': float,
            'julgm2_c': float, 'distm2_c': float, 'suspm2_c': float,
            'julgm2_ant': float, 'distm2_ant': float, 'suspm2_ant': float,
            'julgm4_a': float, 'distm4_a': float, 'suspm4_a': float,
            'julgm4_b': float, 'distm4_b': float, 'suspm4_b': float,
            'julgm6_a': float, 'distm6_a': float, 'suspm6_a': float,
            'julgm7_a': float, 'distm7_a': float, 'suspm7_a': float,
            'julgm7_b': float, 'distm7_b': float, 'suspm7_b': float,
            'julgm8_a': float, 'distm8_a': float, 'suspm8_a': float,
            'julgm8_b': float, 'distm8_b': float, 'suspm8_b': float,
            'julgm10_a': float, 'distm10_a': float, 'suspm10_a': float,
            'julgm10_b': float, 'distm10_b': float, 'suspm10_b': float,
        }
        
        columns_to_read = list(dtypes_explicit.keys())

        df_dask = dd.read_csv(
            caminho_csv,
            blocksize="64MB", 
            dtype=dtypes_explicit, 
            usecols=columns_to_read 
        )

        df_dask['sigla_tribunal'] = df_dask['sigla_tribunal'].fillna('Desconhecido').astype(str)

        def processo_de_particao(partition_df):
            resultados_partition = []
            for tribunal, grupo in partition_df.groupby("sigla_tribunal"):
                resultado_tribunal = {"tribunal": tribunal}
                for meta_name, func in METAS.items():
                    valores = func(grupo)
                    if valores.size > 0:
                        soma = np.nansum(valores)
                        resultado_tribunal[meta_name] = soma
                resultados_partition.append(resultado_tribunal)
            return pd.DataFrame(resultados_partition)

        meta_schema = {'tribunal': object}
        for meta_name in METAS.keys():
            meta_schema[meta_name] = np.float64
            
        df_meta_results = df_dask.map_partitions(
            processo_de_particao, 
            meta=meta_schema 
        )

        # O .compute() aciona o cálculo real em paralelo com Dask
        df_resultado = df_meta_results.groupby("tribunal").agg({meta: 'sum' for meta in METAS.keys()}).reset_index().compute()
        
        df_resultado.to_csv("ResumoMetas.csv", index=False, float_format="%.2f", na_rep="NA")
        print("Arquivo 'ResumoMetas.csv' gerado.")

        # --- Chamada SEQUENCIAL das funções de geração de gráficos ---
        gerar_graficos(df_resultado)
        gerar_grafico_consolidado(df_resultado)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_csv}' não foi encontrado. Verifique o caminho.")
    except ImportError:
        print("Erro: As bibliotecas 'dask' ou 'pyarrow' não estão instaladas. Por favor, instale-as com 'pip install dask[dataframe] pyarrow'.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    print(f"Tempo total de execução: {time.time() - inicio:.2f} segundos")

if __name__ == "__main__":
    main()
