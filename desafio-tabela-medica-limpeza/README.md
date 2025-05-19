# Python para Dados

## Visão Geral

Esta seção do repositório contém todos os scripts, notebooks e arquivos relacionados ao meu aprendizado e prática em Python para análise de dados. O objetivo foi explorar e aplicar conceitos de manipulação, limpeza e análise de dados usando bibliotecas como Pandas, NumPy e SQLite.

## Estrutura do Projeto

A pasta `python-para-dados/` está organizada da seguinte forma:

```

python-para-dados/
├── bases_de_dados_geradas/
│   ├── base_hospital_final.db
│   ├── registro_hospital_1.db
│   ├── registro_hospital_2.db
│   ├── registro_hospital_3.db
│   ├── registro_hospital_4.db
│   └── registro_hospital_5.db
├── bases_de_dados_limpas/
│   └── base_hospital_final_limpa.db
├── notebooks/
│   └── principal.ipynb
└── scripts/
├── gerar_tabelas_raw.py
├── limpeza_registros.py
└── mesclar_bases.py

```

* `bases_de_dados_geradas/`: Contém os arquivos de banco de dados SQLite brutos, gerados pelos scripts.
* `bases_de_dados_limpas/`: Contém os arquivos de banco de dados SQLite limpos, após a remoção de linhas com valores `None`.
* `notebooks/`: Contém o notebook Jupyter (`principal.ipynb`) com análises e explorações dos dados.
* `scripts/`: Contém os scripts Python utilizados para:
    * `gerar_tabelas_raw.py`: Gera os arquivos de banco de dados SQLite com dados fictícios.
    * `mesclar_bases.py`: Faz a junção dos registros fictícios em um único dataset.
    * `limpeza_registros.py`: Remove linhas com valores `None` dos bancos de dados.

## Scripts e Notebooks Principais

* **`gerar_tabelas_raw.py`**: Este script usa as bibliotecas `sqlite3`, `pandas` e outras para gerar dados fictícios para várias tabelas (pacientes, médicos, consultas, etc.) e criar múltiplos arquivos de banco de dados SQLite. Ele garante a unicidade dos IDs primários entre os diferentes arquivos.
* **`limpeza_registros.py`**: Este script lê os arquivos de banco de dados gerados, usa `pandas` para remover as linhas que contêm valores `None` (NULL em SQL) e salva os resultados em novos arquivos de banco de dados "limpos".
* **`mesclar_bases.py`**: Este script combina os dados de múltiplos arquivos de banco de dados em um único banco de dados consolidado.
* **`principal.ipynb`**: Este notebook Jupyter contém a análise exploratória dos dados, visualizações e qualquer outro processamento que tenha sido feito. Ele demonstra como carregar os dados dos arquivos de banco de dados limpos, realizar consultas SQL com `pandas`, criar gráficos e obter insights.

## Como Usar

1.  Os scripts em `scripts/` não devem ser executados diretamente até o momento e sim através do `%rum` do jupyter notebook.
2.  O notebook `principal.ipynb` pode ser aberto no Jupyter para fazer todos os processos e também explorar e analisar os dados gerados.

## Próximos Passos

* Vou tentar melhorar e reutilizar esse código que gera a base de dados fictícia para fazer análize de gráficos.

## Notas

* Os dados gerados são fictícios e destinados apenas para fins de aprendizado e demonstração.
