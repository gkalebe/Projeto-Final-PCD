import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
from numba import jit

#---------------------------------------------------------------- Calculo de Metas --------------------------------------------------------------------------------------

@jit(nopython=True)
def calcular_meta_numba(numerador, denominador, multiplicador):
    
    resultado = np.empty_like(numerador)
    for i in range(len(numerador)):
        # Evita divisão por zero e valores NaN
        if denominador[i] == 0 or np.isnan(numerador[i]) or np.isnan(denominador[i]):
            resultado[i] = np.nan
        else:
            resultado[i] = round((numerador[i] / denominador[i]) * multiplicador, 2)
    return resultado

def calcula_meta_segura(df, num_col, den_cols, multiplicador):

    # Verifica se todas as colunas necessárias estão presentes
    colunas_necessarias = [num_col] + [col.lstrip('-') for col in den_cols]
    if not all(col in df.columns for col in colunas_necessarias):
        return np.array([])
    
    numerador = df[num_col].values
    denominador = np.zeros_like(numerador)
    
    # Soma ou subtrai colunas do denominador conforme prefixo '-'
    for col in den_cols:
        if col.startswith('-'):
            denominador -= df[col.lstrip('-')].values
        else:
            denominador += df[col].values
    
    # Chama função otimizada para cálculo
    return calcular_meta_numba(numerador, denominador, multiplicador)

# Dicionário que mapeia nomes das metas para funções que calculam cada uma
# Cada função recebe um DataFrame e retorna o cálculo da meta correspondente
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

#--------------------------------------------------------  Gera gráficos de barras --------------------------------------------------------------------------------

def gerar_graficos(df):
  
    sns.set(style="whitegrid")
    os.makedirs("GraficosPorTribunal", exist_ok=True)

    for _, row in df.iterrows():
        tribunal = row["tribunal"]
        # Filtra metas presentes e válidas
        metas_presentes = [meta for meta in METAS.keys() if meta in row and not pd.isna(row[meta])]
        valores = row[metas_presentes]
        cores = ['green' if v >= 100 else 'red' for v in valores]

        plt.figure(figsize=(12, 6))
        plt.bar(metas_presentes, valores, color=cores)
        plt.axhline(100, color='gray', linestyle='--', linewidth=1)

        # Anota valores sobre as barras
        for i, v in enumerate(valores):
            label = f"{v:.2f}" if not pd.isna(v) else "NA"
            plt.text(i, v + 1, label, ha='center', va='bottom', fontsize=9)

        plt.title(f"Desempenho nas Metas - {tribunal}")
        plt.ylabel("% de Cumprimento")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"GraficosPorTribunal/grafico_{tribunal}.png")
        plt.close()

 # -------------------------------------------------------------- Função principal do programa ------------------------------------------------------------------------

def main():
    
    inicio = time.time()
    caminho_csv = input("Informe o caminho completo para 'todos_csvs.csv': ").strip().replace('"', '')
    chunk_size = 50000
    resultados = {}

    try:
        # Processa o CSV em pedaços
        for chunk in pd.read_csv(caminho_csv, chunksize=chunk_size):
            chunk.fillna(0, inplace=True)
            # Agrupa por tribunal
            for tribunal, grupo in chunk.groupby("sigla_tribunal"):
                if tribunal not in resultados:
                    resultados[tribunal] = {"tribunal": tribunal}
                # Calcula todas as metas para o grupo
                for meta, func in METAS.items():
                    valores = func(grupo)
                    if valores.size > 0:
                        soma = np.nansum(valores)
                        resultados[tribunal][meta] = resultados[tribunal].get(meta, 0) + soma

        # Converte resultados para DataFrame e salva CSV
        df_resultado = pd.DataFrame(resultados.values())
        df_resultado.to_csv("ResumoMetas.csv", index=False, float_format="%.2f", na_rep="NA")
        print("Arquivo 'ResumoMetas.csv' gerado.")

        # Gera gráficos baseados no resultado
        gerar_graficos(df_resultado)
        print("Gráficos gerados na pasta 'GraficosPorTribunal'.")

    except Exception as e:
        print(f"Erro: {e}")

    print(f"Tempo total de execução: {time.time() - inicio:.2f} segundos")

if __name__ == "__main__":
    main()

