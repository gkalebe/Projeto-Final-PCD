
# 📊 Processamento de CSVs - Análise de Metas do Poder Judiciário

## 🎯 Descrição
Este projeto foi desenvolvido como atividade avaliativa para a disciplina **Programação Concorrente e Paralela** da **Universidade Católica de Brasília - UCB**, no 1º semestre de 2025. O objetivo é realizar o processamento de arquivos CSV para calcular o desempenho dos tribunais brasileiros no cumprimento das metas estabelecidas pelo Poder Judiciário, utilizando as técnicas de ETL (Extract, Transform, Load).

O projeto inclui uma versão sequencial (não paralela) e uma versão paralela, além de gerar arquivos consolidados e gráficos comparativos.

## 🚀 Funcionalidades
- 📥 Extração de dados de múltiplos arquivos CSV.
- 🔄 Transformação dos dados aplicando fórmulas específicas de metas.
- 📤 Geração de arquivos consolidados com os resultados:
  - `ResumoMetas.csv`
  - `Consolidado.csv`
- 📊 Geração de gráfico comparativo entre os tribunais.
- ⚙️ Implementação sequencial e paralela para análise de performance (speedup).

## 🗂️ Estrutura do Projeto
```
📁 Projeto
├── 📄 Versao_NP.py           # Código não paralelo
├── 📄 Versao_P.py            # Código paralelo
├── 📄 Consolidado.csv        # Dados consolidados
├── 📄 ResumoMetas.csv        # Resumo dos resultados
├── 📄 Speedup.pdf            # Relatório de comparação entre as versões
├── 📄 README.md              # Documentação do projeto
└── 📁 dados                  # Pasta contendo os arquivos CSV fornecidos
```

## ⚙️ Requisitos
- Python 3.10+
- Bibliotecas:
  - pandas
  - matplotlib
  - concurrent.futures (biblioteca padrão)

### Instalar dependências
```bash
pip install pandas matplotlib
```

## ▶️ Como Executar

### ✅ Versão Não Paralela
```bash
python Versao_NP.py
```

### ✅ Versão Paralela
```bash
python Versao_P.py
```

### 📈 Saídas Geradas
- `ResumoMetas.csv` → Arquivo com o desempenho de cada tribunal em cada meta.
- `Consolidado.csv` → Arquivo consolidando todos os CSVs originais.
- Gráfico PNG ou exibido em tela comparando desempenhos dos tribunais.

## 📄 Relatório de Speedup
O arquivo `Speedup.pdf` apresenta a análise de desempenho comparando a versão sequencial com a versão paralela, destacando ganhos de tempo na execução.

## 🏛️ Contexto Acadêmico
- 📚 **Disciplina:** Programação Concorrente e Distribuida
- 🏫 **Universidade:** Universidade Católica de Brasília (UCB)
- 👨‍🏫 **Professor:** Marcelo Eustáquio
- 📅 **Período:** 1º semestre de 2025

## 👨‍💻 Autores
