import sqlite3
import pandas as pd
import glob
import os

'''
-- como carregar todas as data bases da pasta "../bases_de_dados_geradas/*.bd" e mesclar em um arquivo base de dados "base_hospital_final.db"

 • [✓] Primeiro carregar as bases e salvar cada tabela no formato de dataFrame em um dicionário e os dicionários em uma lista
 • [✓] salvar em um arquivo "chamado base_hospital_final.db" em "../bases_de_dados_geradas"
'''  

arquivos_dados = glob.glob("../bases_de_dados_geradas/*.db")
print(f"Arquivos carregados {arquivos_dados}")

todas_tabelas = []

todas_tabelas = {}

for arquivo in arquivos_dados:
    DATABASE_NAME = arquivo
    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [row[0] for row in cursor.fetchall()]

    for tabela in tabelas:
        df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
        if tabela not in todas_tabelas:
            todas_tabelas[tabela] = []
        todas_tabelas[tabela].append(df)
        print(f"Do arquivo {os.path.basename(arquivo)}: Tabela '{tabela}' carregada.")

    print(f"\n{f' Tabelas de {os.path.basename(arquivo)} carregadas ':=^60}\n")
    conn.close()

print(f"\n{' Mesclando tabelas e salvando em base_hospital_final.db ':=^60}\n")

DATABASE_FINAL = "../bases_de_dados_geradas/base_hospital_final.db"
conn_final = sqlite3.connect(DATABASE_FINAL)
cursor_final = conn_final.cursor()

for tabela, lista_de_dfs in todas_tabelas.items():
    if lista_de_dfs:
        df_final = pd.concat(lista_de_dfs, ignore_index=True)
        df_final.to_sql(tabela, conn_final, if_exists='replace', index=False)
        print(f"Tabela '{tabela}' mesclada e salva em '{os.path.basename(DATABASE_FINAL)}'.")
    else:
        print(f"Aviso: Nenhuma data encontrado para a tabela '{tabela}'.")

conn_final.close()

print(f"\n{' Processo finalizado com sucesso! ':=^60}\n")
print(f"Base de dados final salva em: {DATABASE_FINAL}")