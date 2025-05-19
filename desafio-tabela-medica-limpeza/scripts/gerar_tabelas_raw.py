import sqlite3
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# --- Variáveis Globais para Controlar IDs ---
paciente_id_counter = 0
medico_id_counter = 0
consulta_id_counter = 0
medicamento_id_counter = 0
prescricao_id_counter = 0
exame_id_counter = 0
solicitacao_id_counter = 0
resultado_id_counter = 0

# --- Variáveis Globais de Listas de Opções ---
especialidades_medicas = ['Clínica Geral', 'Cardiologia', 'Dermatologia', 'Ortopedia', 'Pediatria']
tipos_consulta_lista = ['Rotina', 'Emergência', 'Acompanhamento', 'Primeira Consulta']
motivos_consulta_lista = ['Check-up', 'Dor de cabeça', 'Consulta de rotina', 'Exames', 'Revisão', 'Febre', 'Lesão esportiva']
diagnosticos_lista = ['Saudável', 'Gripe', 'Hipertensão', 'Diabetes', 'Dermatite', 'Fratura', 'Enxaqueca', None]
principios_ativos = ['Paracetamol', 'Ibuprofeno', 'Amoxicilina', None, 'Dipirona', 'Losartana', 'Sinvastatina']
unidades_medida = ['mg', 'ml', 'g', 'UI', None]
frequencias = ['1 vez ao dia', '2 vezes ao dia', None, 'A cada 12 horas', 'Se necessário']
duracoes = ['5 dias', '7 dias', '10 dias', None, '14 dias', '30 dias']
nomes_exames = ['Hemograma Completo', 'Eletrocardiograma (ECG)', None, 'Raio-X Torax', 'Ultrassom Abdominal', 'Tomografia Computadorizada (TC)', 'Ressonância Magnética (RM)']
status_exame = ['Solicitado', None, 'Realizado', 'Cancelado']
unidades_resultado_exames = ['%', 'bpm', None, 'cm', 'mmHg', 'g/dL', '']

# --- Funções Auxiliares ---
def gerar_data_aleatoria(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

def gerar_hora_aleatoria():
    return f"{random.randint(8, 18):02}:{random.randint(0, 59):02}"

def inserir_valor_faltando(valor, probabilidade=0.05):
    """Insere None (NULL em SQL) no lugar do valor com uma dada probabilidade."""
    return None if random.random() < probabilidade else valor

# --- Funções para Gerar Dados de Cada Tabela ---
def gerar_dados_pacientes(num_registros):
    global paciente_id_counter
    pacientes_data = {
        'paciente_id': [paciente_id_counter + i + 1 for i in range(num_registros)],
        'nome_completo': [inserir_valor_faltando(f'Paciente {paciente_id_counter + i + 1}') for i in range(num_registros)],
        'data_nascimento': [gerar_data_aleatoria(datetime(1960, 1, 1), datetime(2005, 12, 31)) for _ in range(num_registros)],
        'sexo': [inserir_valor_faltando(random.choice(['Masculino', 'Feminino'])) for _ in range(num_registros)],
        'endereco': [inserir_valor_faltando(f'Rua {random.randint(1, 100)}, Número {random.randint(1, 500)}') for _ in range(num_registros)],
        'telefone': [inserir_valor_faltando(f'({random.randint(11, 99)}) {random.randint(900000000, 999999999)}') for _ in range(num_registros)],
        'email': [inserir_valor_faltando(f'paciente{paciente_id_counter + i + 1}@email.com') for i in range(num_registros)],
        'plano_saude': [inserir_valor_faltando(random.choice(['Unimed', 'SulAmérica', 'Bradesco Saúde', None])) for _ in range(num_registros)]
    }
    paciente_id_counter += num_registros
    return pd.DataFrame(pacientes_data)

def gerar_dados_medicos(num_registros):
    global medico_id_counter
    medicos_data = {
        'medico_id': [medico_id_counter + i + 1 for i in range(num_registros)],
        'nome_completo': [inserir_valor_faltando(f'Médico {medico_id_counter + i + 1}') for i in range(num_registros)],
        'especialidade': [inserir_valor_faltando(random.choice(especialidades_medicas)) for _ in range(num_registros)],
        'crm': [inserir_valor_faltando(f'{random.randint(10000, 99999)}/{random.choice(["SP", "RJ"])}') for _ in range(num_registros)],
        'telefone': [inserir_valor_faltando(f'({random.randint(11, 99)}) {random.randint(900000000, 999999999)}') for _ in range(num_registros)],
        'email': [inserir_valor_faltando(f'medico{medico_id_counter + i + 1}@hospital.com') for i in range(num_registros)]
    }
    medico_id_counter += num_registros
    return pd.DataFrame(medicos_data)

def gerar_dados_consultas(num_registros, df_pacientes, df_medicos):
    global consulta_id_counter
    consultas_data = {
        'consulta_id': [consulta_id_counter + i + 1 for i in range(num_registros)],
        'paciente_id': np.random.choice(df_pacientes['paciente_id'], num_registros) if not df_pacientes.empty else None,
        'medico_id': np.random.choice(df_medicos['medico_id'], num_registros) if not df_medicos.empty else None,
        'data_consulta': [gerar_data_aleatoria(datetime(2024, 1, 1), datetime(2025, 5, 18)) for _ in range(num_registros)],
        'hora_consulta': [inserir_valor_faltando(gerar_hora_aleatoria()) for _ in range(num_registros)],
        'tipo_consulta': [inserir_valor_faltando(random.choice(tipos_consulta_lista)) for _ in range(num_registros)],
        'motivo_consulta': [inserir_valor_faltando(random.choice(motivos_consulta_lista)) for _ in range(num_registros)],
        'diagnostico_principal': [inserir_valor_faltando(random.choice(diagnosticos_lista)) for _ in range(num_registros)]
    }
    consulta_id_counter += num_registros
    return pd.DataFrame(consultas_data)

def gerar_dados_medicamentos(num_registros):
    global medicamento_id_counter
    medicamentos_data = {
        'medicamento_id': [medicamento_id_counter + i + 1 for i in range(num_registros)],
        'nome_comercial': [inserir_valor_faltando(f'Medicamento {chr(ord("A") + i % 26)}{i // 26 + 1}') for i in range(num_registros)],
        'principio_ativo': [inserir_valor_faltando(random.choice(principios_ativos)) for _ in range(num_registros)],
        'dosagem': [inserir_valor_faltando(f'{random.randint(10, 500)}') for _ in range(num_registros)],
        'unidade_medida': [inserir_valor_faltando(random.choice(unidades_medida)) for _ in range(num_registros)]
    }
    medicamento_id_counter += num_registros
    return pd.DataFrame(medicamentos_data)

def gerar_dados_prescricoes(num_registros, df_consultas, df_medicamentos):
    global prescricao_id_counter
    prescricoes_data = {
        'prescricao_id': [prescricao_id_counter + i + 1 for i in range(num_registros)],
        'consulta_id': np.random.choice(df_consultas['consulta_id'], num_registros) if not df_consultas.empty else None,
        'medicamento_id': np.random.choice(df_medicamentos['medicamento_id'], num_registros) if not df_medicamentos.empty else None,
        'dosagem_prescrita': [inserir_valor_faltando(f'{random.randint(1, 2)} comprimido(s)') for _ in range(num_registros)],
        'frequencia': [inserir_valor_faltando(random.choice(frequencias)) for _ in range(num_registros)],
        'duracao_tratamento': [inserir_valor_faltando(random.choice(duracoes)) for _ in range(num_registros)]
    }
    prescricao_id_counter += num_registros
    return pd.DataFrame(prescricoes_data)

def gerar_dados_exames(num_registros):
    global exame_id_counter
    exames_data = {
        'exame_id': [exame_id_counter + i + 1 for i in range(num_registros)],
        'nome_exame': [inserir_valor_faltando(random.choice(nomes_exames)) for _ in range(num_registros)],
        'descricao': [inserir_valor_faltando(f'Descrição do exame {exame_id_counter + i + 1}') for i in range(num_registros)]
    }
    exame_id_counter += num_registros
    return pd.DataFrame(exames_data)

def gerar_dados_solicitacoes_exames(num_registros, df_consultas, df_exames):
    global solicitacao_id_counter
    solicitacoes_exames_data = {
        'solicitacao_id': [solicitacao_id_counter + i + 1 for i in range(num_registros)],
        'consulta_id': np.random.choice(df_consultas['consulta_id'], num_registros) if not df_consultas.empty else None,
        'exame_id': np.random.choice(df_exames['exame_id'], num_registros) if not df_exames.empty else None,
        'data_solicitacao': [gerar_data_aleatoria(datetime(2024, 1, 1), datetime(2025, 5, 18)) for _ in range(num_registros)],
        'status': [inserir_valor_faltando(random.choice(status_exame)) for _ in range(num_registros)]
    }
    solicitacao_id_counter += num_registros
    return pd.DataFrame(solicitacoes_exames_data)

def gerar_dados_resultados_exames(num_registros, df_solicitacoes_exames):
    global resultado_id_counter
    resultados_exames_data = {
        'resultado_id': [resultado_id_counter + i + 1 for i in range(num_registros)],
        'solicitacao_id': np.random.choice(df_solicitacoes_exames['solicitacao_id'], num_registros, replace=False) if not df_solicitacoes_exames.empty and len(df_solicitacoes_exames) >= num_registros else (np.random.choice(df_solicitacoes_exames['solicitacao_id'], num_registros, replace=True) if not df_solicitacoes_exames.empty else None),
        'data_realizacao': [gerar_data_aleatoria(datetime(2024, 1, 1), datetime(2025, 5, 18)) for _ in range(num_registros)],
        'resultado': [inserir_valor_faltando(str(np.random.randint(1, 200))) if random.random() > 0.4 else inserir_valor_faltando('Normal') for _ in range(num_registros)],
        'unidade_resultado': [inserir_valor_faltando(random.choice(unidades_resultado_exames)) for _ in range(num_registros)],
        'valor_referencia': [inserir_valor_faltando(f'{random.randint(10, 100)}-{random.randint(110, 200)}') if random.random() > 0.6 else inserir_valor_faltando('Dentro dos limites') for _ in range(num_registros)]
    }
    resultado_id_counter += num_registros
    return pd.DataFrame(resultados_exames_data)

# --- Função Principal para Gerar e Salvar o Banco de Dados ---
def criar_banco_dados_medico(nome_base="minha_base_medica_personalizada", num_bases=1, config_registros=None, output_dir="bases_medicas"):
    """
    Cria múltiplos arquivos de banco de dados SQLite com dados médicos.

    Args:
        nome_base (str): O nome base para os arquivos de banco de dados.
        num_bases (int): O número de arquivos de banco de dados a serem gerados.
        config_registros (dict): Um dicionário especificando o número de registros para cada tabela.
        output_dir (str): O nome do diretório onde os arquivos de banco de dados serão salvos.
    """
    if config_registros is None:
        config_registros = {
            'pacientes': 30,
            'medicos': 15,
            'consultas': 50,
            'medicamentos': 20,
            'prescricoes': 40,
            'exames': 18,
            'solicitacoes_exames': 45,
            'resultados_exames': 35
        }

    # Cria o diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Diretório '{output_dir}' criado.")

    for i in range(1, num_bases + 1):
        nome_arquivo_db = os.path.join(output_dir, f"{nome_base}_{i}.db")
        print(f"\n--- Gerando dados para o banco de dados: {nome_arquivo_db} ---")

        print("Gerando dados...")
        df_pacientes = gerar_dados_pacientes(config_registros.get('pacientes', 0))
        df_medicos = gerar_dados_medicos(config_registros.get('medicos', 0))
        df_consultas = gerar_dados_consultas(config_registros.get('consultas', 0), df_pacientes, df_medicos)
        df_medicamentos = gerar_dados_medicamentos(config_registros.get('medicamentos', 0))
        df_prescricoes = gerar_dados_prescricoes(config_registros.get('prescricoes', 0), df_consultas, df_medicamentos)
        df_exames = gerar_dados_exames(config_registros.get('exames', 0))
        df_solicitacoes_exames = gerar_dados_solicitacoes_exames(config_registros.get('solicitacoes_exames', 0), df_consultas, df_exames)
        df_resultados_exames = gerar_dados_resultados_exames(config_registros.get('resultados_exames', 0), df_solicitacoes_exames)

        print(f"Salvando dados no banco de dados: {nome_arquivo_db}")
        conn = sqlite3.connect(nome_arquivo_db)

        df_pacientes.to_sql('pacientes', conn, if_exists='replace', index=False)
        df_medicos.to_sql('medicos', conn, if_exists='replace', index=False)
        df_consultas.to_sql('consultas', conn, if_exists='replace', index=False)
        df_medicamentos.to_sql('medicamentos', conn, if_exists='replace', index=False)
        df_prescricoes.to_sql('prescricoes', conn, if_exists='replace', index=False)
        df_exames.to_sql('exames', conn, if_exists='replace', index=False)
        df_solicitacoes_exames.to_sql('solicitacoes_exames', conn, if_exists='replace', index=False)
        df_resultados_exames.to_sql('resultados_exames', conn, if_exists='replace', index=False)

        conn.close()
        print(f"Bases de dados médicas com dados faltando salvas em '{nome_arquivo_db}'")
        print("Número de registros gerados:")
        print(f"- Pacientes: {len(df_pacientes)}")
        print(f"- Médicos: {len(df_medicos)}")
        print(f"- Consultas: {len(df_consultas)}")
        print(f"- Medicamentos: {len(df_medicamentos)}")
        print(f"- Prescrições: {len(df_prescricoes)}")
        print(f"- Exames: {len(df_exames)}")
        print(f"- Solicitações de Exames: {len(df_solicitacoes_exames)}")
        print(f"- Resultados de Exames: {len(df_resultados_exames)}")

if __name__ == "__main__":
    print("--- Geração de Múltiplos Bancos de Dados Médicos Fictícios ---")

    num_bases_gerar = int(input("Digite o número de bancos de dados a serem gerados: ") or 3)
    nome_base_arquivo = input("Digite o nome base para os arquivos de banco de dados (ex: minha_base_medica): ") or "minha_base_medica_personalizada"

    configuracao_padrao_registros = {
        'pacientes': 200,
        'medicos': random.randint(50, 100),
        'consultas': random.randint(400, 800),
        'medicamentos': random.randint(150, 300),
        'prescricoes': random.randint(300, 600),
        'exames': random.randint(50, 100),
        'solicitacoes_exames': random.randint(250, 500),
        'resultados_exames': random.randint(200, 400)
    }

    configuracao_personalizada = {}
    if input("Deseja personalizar o número de registros para cada tabela? (s/n): ").lower() == 's':
        configuracao_personalizada['pacientes'] = int(input(f"Digite o número de pacientes (padrão: {configuracao_padrao_registros['pacientes']}): ") or configuracao_padrao_registros['pacientes'])
        configuracao_personalizada['medicos'] = int(input(f"Digite o número de médicos (padrão: {configuracao_padrao_registros['medicos']}): ") or configuracao_padrao_registros['medicos'])
        configuracao_personalizada['consultas'] = int(input(f"Digite o número de consultas (padrão: {configuracao_padrao_registros['consultas']}): ") or configuracao_padrao_registros['consultas'])
        configuracao_personalizada['medicamentos'] = int(input(f"Digite o número de medicamentos (padrão: {configuracao_padrao_registros['medicamentos']}): ") or configuracao_padrao_registros['medicamentos'])
        configuracao_personalizada['prescricoes'] = int(input(f"Digite o número de prescrições (padrão: {configuracao_padrao_registros['prescricoes']}): ") or configuracao_padrao_registros['prescricoes'])
        configuracao_personalizada['exames'] = int(input(f"Digite o número de exames (padrão: {configuracao_padrao_registros['exames']}): ") or configuracao_padrao_registros['exames'])
        configuracao_personalizada['solicitacoes_exames'] = int(input(f"Digite o número de solicitações de exames (padrão: {configuracao_padrao_registros['solicitacoes_exames']}): ") or configuracao_padrao_registros['solicitacoes_exames'])
        configuracao_personalizada['resultados_exames'] = int(input(f"Digite o número de resultados de exames (padrão: {configuracao_padrao_registros['resultados_exames']}): ") or configuracao_padrao_registros['resultados_exames'])
    else:
        configuracao_personalizada = configuracao_padrao_registros

    # Define o nome do diretório para salvar os bancos de dados
    nome_diretorio_output = "../bases_de_dados_geradas"

    # Chama a função principal para criar os bancos de dados
    criar_banco_dados_medico(
        nome_base=nome_base_arquivo,
        num_bases=num_bases_gerar,
        config_registros=configuracao_personalizada,
        output_dir=nome_diretorio_output
    )

    print("\n--- Geração Concluída ---")