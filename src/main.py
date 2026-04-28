from src.core.logging_config import setup_logging
setup_logging()

import logging
import os
from fastapi import FastAPI
from src.api import routes
from src.process import load_data
from src.db import create_table, insert_data
import src.queries as queries

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(routes.router)

def main():

    logger.info("Iniciando pipeline")

    # Caminho do arquivo CSV
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "vendas.csv")

    # 1 - Carregar os dados
    data = load_data(file_path)

    if not data:

        logger.warning("Nenhum dado para processar. Encerrando pipeline.")
        return

    # 2. Garantir que a tabela existe
    create_table()

    # 3. Inserir os dados na tabela
    insert_data(data)

    # 4. Rodar consultas e gerar relatórios
    all_sales = queries.fetch_by()
    print(f"Total de vendas: {len(all_sales)}")

    lucca_sales = queries.fetch_by_cliente("Lucca")
    print(f"Vendas do Lucca: {len(lucca_sales)}")

    summary = queries.fetch_report()
    print(f"Resumo: {summary['total_sales']} vendas, totalizando R${summary['total_value']:.2f}")

    logger.info("Pipeline finalizado com sucesso")

if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        logger.error(f"Erro fatal inesperado: {e}")