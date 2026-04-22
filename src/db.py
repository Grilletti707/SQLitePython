import sqlite3
import os

# Ajustando os caminhos da criação da db, para garantir que vai ficar organizado
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "database.db")

# Conferindo se /db existe
os.makedirs(DB_DIR, exist_ok=True)


def get_connection(): # Pensando em escalabilidade e boa prática, é melhor colocar como uma função

    try:
        # Criando uma conexão com a db no caminho ajustado (/db)
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e: #Tratamento de erro
        print(f"Erro ao conectar no banco: {e}")
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

    except Exception as e:
        print(f"Erro ao criar tabela: {e}")

    finally:
        conn.close()

def insert_data(data):
    