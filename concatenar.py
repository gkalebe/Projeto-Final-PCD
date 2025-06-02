import pandas as pd
import os 
import time

pasta_csv = r"C:\Programação\Python\PCD\projeto_final\Dados"
lista_dataframe = []

t_inicial = time.time()

for nome_arquivo in os.listdir(pasta_csv):
    if nome_arquivo.endswith(".csv"):
        caminho = os.path.join(pasta_csv, nome_arquivo)
        

        df = pd.read_csv(caminho, low_memory=False, engine='c', dtype=str)
        lista_dataframe.append(df)

df_concatenando = pd.concat(lista_dataframe, ignore_index=True)


df_concatenando.to_csv("todos_csvs.csv", index=False)

t_final = time.time()

print("Arquivos concatenados com sucesso")
print(f"Tempo total {(t_final - t_inicial)/60:.2f} minutos")
