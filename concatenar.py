import pandas as pd
import os 

pasta_csv = r"C:\Programação\Python\PCD\projeto_final\Dados"
lista_dataframe = []

for nome_arquivo in os.listdir(pasta_csv):
    if nome_arquivo.endswith(".csv"):
        caminho = os.path.join(pasta_csv, nome_arquivo)

        df = pd.read_csv(caminho)

        lista_dataframe.append(df)

df_concatenando = pd.concat(lista_dataframe, ignore_index=True)
df_concatenando.to_csv("todos_csvs.csv", index=True)

print("Arquivos concatenados com sucesso")