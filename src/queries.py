import logging
from typing import List, Dict

from fastapi import params
from src.db import get_connection

def fetch_all(cliente=None, valor_min=None, valor_max=None, data=None) -> List[Dict]: # Relata todas as vendas

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM vendas WHERE 1=1" # Base da query, para facilitar adição de filtros
    params = []

    if cliente is not None:
        print("Filtrando por cliente:", cliente)
        query += " AND cliente LIKE ?"
        params.append(f"%{cliente}%")

    if valor_min is not None:
        query += " AND valor >= ?"
        params.append(valor_min)

    if valor_max is not None:
        query += " AND valor <= ?"
        params.append(valor_max)

    if data is not None:
        query += " AND data = ?"
        params.append(data)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "cliente": row[1],
            "produto": row[2],
            "valor": row[3],
            "data": row[4]
        }
        for row in rows
    ]

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

def fetch_by_id(id: int) -> Dict: # Busca venda por ID

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendas WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        else:
            return {}
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados por ID: {e}")
        return {}
    
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

def delete_by_id(id: int) -> bool: # Deleta venda por ID

    conn = get_connection()
    rows_deleted = 0

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id = ?", (id,))
        conn.commit()
        rows_deleted = cursor.rowcount
        return rows_deleted > 0
    
    except Exception as e:
        logging.error(f"Erro ao deletar venda por ID: {e}")
        return False
    
    finally:
        conn.close()