import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import zipfile


#  Descompactar os arquivos CSV
with zipfile.ZipFile('Dados (1).zip', 'r') as zip_ref:
    zip_ref.extractall('dados')


#  Ler e consolidar os CSVs
pasta_dados = 'dados'
arquivos_csv = [arq for arq in os.listdir(pasta_dados) if arq.endswith('.csv')]
lista_df = []

for arquivo in arquivos_csv:
    caminho = os.path.join(pasta_dados, arquivo)
    try:
        df = pd.read_csv(caminho, encoding='utf-8', sep=';')
    except:
        df = pd.read_csv(caminho, encoding='latin1', sep=';')
    df['fonte_arquivo'] = arquivo
    lista_df.append(df)

consolidado_df = pd.concat(lista_df, ignore_index=True)
consolidado_df.to_csv('Consolidado.csv', index=False, encoding='utf-8', sep=';')

print(" Consolidado.csv gerado com sucesso (paralelo)!")


#  Cálculo Paralelo das Metas
df = pd.read_csv('Consolidado.csv', sep=';', encoding='utf-8')
tribunais = df['ramo_justica'].unique()


def calcular_metas_tribunal(tribunal):
    df_tribunal = df[df['ramo_justica'] == tribunal]

    def meta(julgados, distribuidores, suspensos, fator):
        try:
            julgados_soma = df_tribunal[julgados].sum()
            distribuidores_soma = sum([df_tribunal[col].sum() for col in distribuidores])
            suspensos_soma = df_tribunal[suspensos].sum()

            divisor = distribuidores_soma - suspensos_soma
            if divisor == 0:
                return 'NA'
            resultado = (julgados_soma / divisor) * fator
            return round(resultado, 2)
        except KeyError:
            return 'NA'

    resultado = {
        'ramo_justica': tribunal,
        'Meta1': meta('julgados_2025', ['casos_novos_2025', 'dessobrestados_2025'], 'suspensos_2025', 100)
    }

    metas_parametros = {
        'Meta2A': (1000/8),
        'Meta2B': (1000/9),
        'Meta2C': (1000/9.5),
        'Meta2ANT': 100,
        'Meta4A': (1000/6.5),
        'Meta4B': 100,
        'Meta6': 100,
        'Meta7A': (1000/5),
        'Meta7B': (1000/5),
        'Meta8A': (1000/7.5),
        'Meta8B': (1000/9),
        'Meta10A': (1000/9),
        'Meta10B': (1000/10)
    }

    for meta_nome, fator in metas_parametros.items():
        resultado[meta_nome] = meta('julgados_2025', ['distribuidos_2025'], 'suspensos_2025', fator)

    return resultado


resultados = []

print('🚀 Iniciando processamento paralelo...')

with ProcessPoolExecutor() as executor:
    tarefas = {executor.submit(calcular_metas_tribunal, tribunal): tribunal for tribunal in tribunais}

    for future in as_completed(tarefas):
        tribunal = tarefas[future]
        try:
            resultado = future.result()
            resultados.append(resultado)
            print(f" Concluído: {tribunal}")
        except Exception as e:
            print(f" Erro no tribunal {tribunal}: {e}")


df_resumo = pd.DataFrame(resultados)
df_resumo.to_csv('ResumoMetas.csv', index=False, sep=';', encoding='utf-8')

print(" ResumoMetas.csv gerado com sucesso (paralelo)!")
