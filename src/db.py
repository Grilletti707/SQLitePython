import sqlite3
import os
import logging
from typing import List, Dict

# Ajustando os caminhos da criação da db, para garantir que vai ficar organizado em qualquer máquina, independente do sistema operacional.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "database.db")

# Conferindo se /db existe
os.makedirs(DB_DIR, exist_ok=True)

def get_connection(): # Pensando em escalabilidade e boa prática, é melhor colocar como uma função

    try:
        # Criando uma conexão com a db no caminho ajustado (/db)
        conn = sqlite3.connect(DB_PATH)
        logging.info("Conexão com db estabelecida com sucesso")
        return conn
    
    except Exception as e: #Tratamento de erro
        logging.error(f"Erro ao conectar no banco: {e}")
        return None
    
def create_table():
    
    # Criando uma nova conexão
    conn = get_connection()

    # Criando um cursor
    cursor = conn.cursor()

    try:
        # Criando a tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY,
            cliente TEXT,
            produto TEXT,
            valor REAL,
            data TEXT
        )
        """)

        # "Rodar" o comando de fato
        conn.commit()
        logging.info("Tabela criada com sucesso")

    except Exception as e:
        logging.error(f"Erro ao criar tabela: {e}")

    finally:
        conn.close()

def insert_data(data: List[Dict]):

    conn = get_connection()

    inserted_count = 0
    ignored_count = 0
    failed_count = 0
    errors = []

    try:
        cursor = conn.cursor()

        logging.info("Iniciando inserção de dados")

        for item in data:
            try:
                cursor.execute("""
                INSERT OR IGNORE INTO vendas (id, cliente, produto, valor, data)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    item["id"],
                    item["cliente"],
                    item["produto"],
                    item["valor"],
                    item["data"]
                ))

                if cursor.rowcount == 1:
                    inserted_count += 1
                else:
                    ignored_count += 1

            except Exception as e:
                errors.append({"item": item, "error": str(e)})
                logging.error(f"Erro ao inserir registro: {e}")
                failed_count += 1

        logging.info("Inserção concluída com sucesso")
        conn.commit()

    except Exception as e:
        logging.error(f"Erro geral ao inserir dados: {e}")

    finally:
        conn.close()

    return {
        "inserted": inserted_count,
        "ignored": ignored_count,
        "failed": failed_count,
        "errors": errors
    }