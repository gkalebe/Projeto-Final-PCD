<<<<<<< HEAD
import pandas as pd
import os 
import time

pasta_csv = r"C:\Programação\Python\PCD\projeto_final\Dados"
lista_dataframe = []
t_inicial =time.time()
for nome_arquivo in os.listdir(pasta_csv):
    if nome_arquivo.endswith(".csv"):
        caminho = os.path.join(pasta_csv, nome_arquivo)g

        df = pd.read_csv(caminho)

        lista_dataframe.append(df)

df_concatenando = pd.concat(lista_dataframe, ignore_index=True)
df_concatenando.to_csv("todos_csvs.csv", index=True)
t_final =time.time()

print("Arquivos concatenados com sucesso")
print(f"tempo total {(t_final - t_inicial)/60:.2f} minutos")
=======
>>>>>>> e023996eef8ecdca78f4310bd687ca0efcb47492
