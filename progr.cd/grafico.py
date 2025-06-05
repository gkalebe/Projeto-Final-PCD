import matplotlib.pyplot as plt

# Dados de exemplo
tempos = [18.4, 6.2]  # Substitua pelos seus dados
versoes = ['Não Paralelo', 'Paralelo']

plt.figure(figsize=(8, 5))
plt.bar(versoes, tempos, color=['red', 'green'])
plt.title('Comparação de Tempo de Execução')
plt.ylabel('Tempo (segundos)')
plt.xlabel('Versão')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('grafico_speedup.png')
plt.show()
