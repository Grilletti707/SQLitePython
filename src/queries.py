import sqlite3
import logging
from typing import List, Dict
from db import get_connection

def fetch_all() -> List[Dict]: # Relata todas as vendas

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendas")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados: {e}")
        return []
    
    finally:
        conn.close()

def fetch_by_cliente(cliente: str) -> List[Dict]: # Busca vendas por nome do cliente

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendas WHERE cliente = ?", (cliente,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados por cliente: {e}")
        return []
    
    finally:
        conn.close()

def fetch_summary() -> Dict: # Agrega métricas como total de vendas e valor total

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total_vendas, SUM(valor) AS total_valor FROM vendas")
        row = cursor.fetchone()
        return {"total_vendas": row[0], "total_valor": row[1]}
    
    except Exception as e:
        logging.error(f"Erro ao buscar resumo de vendas: {e}")
        return {"total_vendas": 0, "total_valor": 0.0}
    
    finally:
        conn.close()