import logging
from typing import List, Dict

from fastapi import params
from src.db import get_connection

def fetch_by(cliente=None, valor_min=None, valor_max=None, data=None, limit=None, offset=None) -> List[Dict]: # Relata todas as vendas

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

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    if offset is not None:
        query += " OFFSET ?"
        params.append(offset)

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

def fetch_report() -> Dict: # Agrega métricas como total de vendas e valor total

    conn = get_connection()

    try:
        cursor = conn.cursor()

        query = """
            SELECT 
                COUNT(*) AS total_vendas_loja, --total_sales
                SUM(valor) AS total_valor_loja, --total_value
                (SELECT cliente FROM vendas GROUP BY cliente ORDER BY SUM(valor) DESC LIMIT 1) AS cliente_maior_faturamento, --best_client
                (SELECT cliente FROM vendas GROUP BY cliente ORDER BY COUNT(*) DESC LIMIT 1) AS cliente_mais_fiel, --most_loyal_client
                (SELECT produto FROM vendas GROUP BY produto ORDER BY SUM(valor) DESC LIMIT 1) AS produto_campeao_faturamento, --most_profitable_product
                (SELECT produto FROM vendas GROUP BY produto ORDER BY COUNT(*) DESC LIMIT 1) AS produto_mais_vendido --most_sold_product
            FROM vendas
            LIMIT 1;
        """

        cursor.execute(query)

        row = cursor.fetchone()
        return {
            "total_sales": row[0],              # total_vendas_loja
            "total_value": row[1],              # total_valor_loja
            "best_client": row[2],              # cliente_maior_faturamento
            "most_loyal_client": row[3],        # cliente_mais_fiel
            "most_profitable_product": row[4],  # produto_campeao_faturamento
            "most_sold_product": row[5]         # produto_mais_vendido
        }

    except Exception as e:
        logging.error(f"Erro ao buscar resumo de vendas: {e}")
        return {
            "total_sales": 0, "total_value": 0.0
        }
    
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