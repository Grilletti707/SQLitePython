import csv
import logging
from typing import List, TypedDict
from io import StringIO

# Configurando o logger para este módulo
logger = logging.getLogger(__name__)

class Venda(TypedDict):
    id: int
    cliente: str
    produto: str
    valor: float
    data: str

def _parse_row(row: dict) -> Venda:

    venda: Venda = {
        "id": int(row["id"]),
        "cliente": row["cliente"].strip().title(),
        "produto": row["produto"].strip().title(),
        "valor": float(row["valor"]),
        "data": row["data"]
    }

    # Validação simples para garantir que os dados estão corretos
    if venda["id"] <= 0 or venda["valor"] <= 0:
        raise ValueError("ID deve ser positivo e valor deve ser não negativo")

    return venda

def load_data(file_path: str) -> List[Venda]: # Ler o csv e transformar em uma lista de dicionários, com validação simples dos dados

    data = []

    logger.info(f"Lendo arquivos do caminho: {file_path}")

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    venda = _parse_row(row)
                    data.append(venda)

                except ValueError as ve:
                    logger.error(f"Erro de validação para linha {row} | {ve}")

    except Exception as e:
        logger.error(f"Erro ao ler arquivo: {e}")

    logger.info(f"Total de registros carregados: {len(data)}")

    return data

def process_csv(content: str):

    reader = csv.DictReader(StringIO(content))

    data = []

    for row in reader:

        try:
            item = _parse_row(row)
            data.append(item)

        except ValueError as ve:
            logger.error(f"Linha inválida ignorada: {row} | {ve}")

    return data