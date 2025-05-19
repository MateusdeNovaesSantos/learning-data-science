import sqlite3
import pandas as pd
import os
import datetime

def remover_linhas_com_none_e_salvar(input_db_path, output_db_path):
    """
    Percorre todas as tabelas em um banco de dados SQLite de entrada,
    remove as linhas com valores None (NaN) e salva as tabelas limpas
    em um novo arquivo de banco de dados SQLite de saída.

    Args:
        input_db_path (str): O caminho para o arquivo do banco de dados SQLite de entrada.
        output_db_path (str): O caminho para o arquivo do banco de dados SQLite de saída.
    """
    conn_in = sqlite3.connect(input_db_path)
    conn_out = sqlite3.connect(output_db_path)
    cursor_in = conn_in.cursor()

    # Obter a lista de todas as tabelas no banco de dados de entrada
    cursor_in.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [row[0] for row in cursor_in.fetchall()]

    for tabela in tabelas:
        print(f"Processando tabela: {tabela} do arquivo: {os.path.basename(input_db_path)}")

        # Ler a tabela para um DataFrame do Pandas
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn_in)
        initial_rows = len(df)

        # Remover linhas com qualquer valor None (NaN)
        df_cleaned = df.dropna()
        rows_dropped = initial_rows - len(df_cleaned)

        # Salvar o DataFrame limpo no novo banco de dados
        df_cleaned.to_sql(tabela, conn_out, if_exists='replace', index=False)
        print(f"  Tabela '{tabela}' limpa ({rows_dropped} linhas removidas) e salva em: {os.path.basename(output_db_path)}")

    conn_in.close()
    conn_out.close()
    print(f"\nProcesso de limpeza e salvamento concluído.")
    print(f"Dados limpos salvos em: {output_db_path}")

if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_entrada = "../bases_de_dados_geradas/base_hospital_final.db"
    arquivo_saida = f"../bases_de_dados_limpas/base_hospital_final_limpa_{timestamp}.db"

    # Criar a pasta de saída se não existir
    pasta_saida = os.path.dirname(arquivo_saida)
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"Pasta de saída criada: {pasta_saida}")

    if os.path.exists(arquivo_entrada):
        print(f"Processando arquivo de entrada: {arquivo_entrada}")
        remover_linhas_com_none_e_salvar(arquivo_entrada, arquivo_saida)
    else:
        print(f"Arquivo de entrada não encontrado: {arquivo_entrada}")