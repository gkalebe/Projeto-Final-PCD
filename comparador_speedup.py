import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt

# Nomes dos scripts que vamos rodar
VERSAO_SEQ = "Versao_NP.py"
VERSAO_PAR = "Versao_P.py"
ARQUIVO_SPEEDUP = "SpeedupComparativo.csv"

def medir_tempo_execucao(script):
    # Marca o tempo antes de rodar o script
    inicio = time.time()
    subprocess.run(["python", script], check=True)
    # Marca o tempo depois
    fim = time.time()
    # Calcula e retorna o tempo que levou para rodar
    return round(fim - inicio, 2)

print("Rodando a versão sequencial...")
tempo_seq = medir_tempo_execucao(VERSAO_SEQ)

print("Rodando a versão paralela...")
tempo_par = medir_tempo_execucao(VERSAO_PAR)

# Calcula o speedup (quanto a paralela foi mais rápida)
speedup = round(tempo_seq / tempo_par, 2) if tempo_par > 0 else 'Inf'

# Cria um DataFrame com os resultados e salva em CSV
df_speedup = pd.DataFrame([{
    'tempo_sequencial': tempo_seq,
    'tempo_paralelo': tempo_par,
    'speedup': speedup
}])
df_speedup.to_csv(ARQUIVO_SPEEDUP, index=False)
print(f"Resultados salvos em {ARQUIVO_SPEEDUP}")

# Gera um gráfico comparando os tempos
plt.figure(figsize=(6, 4))
plt.bar(['Sequencial', 'Paralela'], [tempo_seq, tempo_par], color=['orange', 'green'])
plt.title(f"Speedup: {speedup}x")
plt.ylabel("Tempo (segundos)")
plt.savefig("grafico_speedup.png")
print("Gráfico 'grafico_speedup.png' criado com sucesso.")
