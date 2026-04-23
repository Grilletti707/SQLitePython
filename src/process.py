import csv
import logging
from typing import List, TypedDict

class Venda(TypedDict):
    id: int
    cliente: str
    produto: str
    valor: float
    data: str

def load_data(file_path: str) -> List[Venda]:

    data = []

    logging.info(f"Lendo arquivos do caminho: {file_path}")

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            
            reader = csv.DictReader(csvfile)

            for row in reader:

                try:
                    venda: Venda = {
                        "id": int(row["id"]),
                        "cliente": row["cliente"].strip().title(),
                        "produto": row["produto"].strip().title(),
                        "valor": float(row["valor"]),
                        "data": row["data"]
                    }

                    # Validação simples para garantir que os dados estão corretos
                    if venda["id"] <= 0:
                        raise ValueError("ID deve ser positivo")

                    data.append(venda)

                except ValueError as ve:
                    logging.error(f"Erro de validação para linha {row} | {ve}")

    except Exception as e:
        logging.error(f"Erro ao ler arquivo: {e}")

    logging.info(f"Total de registros carregados: {len(data)}")

    return data