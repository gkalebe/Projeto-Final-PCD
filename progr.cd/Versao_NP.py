import pandas as pd
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

print(" Consolidado.csv gerado com sucesso!")



#  Cálculo das Metas
df = pd.read_csv('Consolidado.csv', sep=';', encoding='utf-8')
tribunais = df['ramo_justica'].unique()

resultado = {
    'ramo_justica': [],
    'Meta1': [],
    'Meta2A': [],
    'Meta2B': [],
    'Meta2C': [],
    'Meta2ANT': [],
    'Meta4A': [],
    'Meta4B': [],
    'Meta6': [],
    'Meta7A': [],
    'Meta7B': [],
    'Meta8A': [],
    'Meta8B': [],
    'Meta10A': [],
    'Meta10B': []
}


def calcular_meta(df, julgados, distribuidores, suspensos, fator):
    try:
        julgados_soma = df[julgados].sum()
        distribuidores_soma = sum([df[col].sum() for col in distribuidores])
        suspensos_soma = df[suspensos].sum()

        divisor = distribuidores_soma - suspensos_soma
        if divisor == 0:
            return 'NA'
        resultado = (julgados_soma / divisor) * fator
        return round(resultado, 2)
    except KeyError:
        return 'NA'


for tribunal in tribunais:
    df_tribunal = df[df['ramo_justica'] == tribunal]

    resultado['ramo_justica'].append(tribunal)

    # Meta 1
    m1 = calcular_meta(df_tribunal, 'julgados_2025',
                        ['casos_novos_2025', 'dessobrestados_2025'], 'suspensos_2025', 100)
    resultado['Meta1'].append(m1)

    # Metas gerais
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

    for meta, fator in metas_parametros.items():
        valor = calcular_meta(df_tribunal, 'julgados_2025',
                              ['distribuidos_2025'], 'suspensos_2025', fator)
        resultado[meta].append(valor)


df_resumo = pd.DataFrame(resultado)
df_resumo.to_csv('ResumoMetas.csv', index=False, sep=';', encoding='utf-8')

print(" ResumoMetas.csv gerado com sucesso!")
