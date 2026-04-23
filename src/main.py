import logging
from process import load_data
from db import create_table, insert_data
import os

def main():

    logging.info("Iniciando pipeline")

    # Caminho do arquivo CSV
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "vendas.csv")

    # 1 - Carregar os dados
    data = load_data(file_path)

    if not data:

        logging.warning("Nenhum dado para processar. Encerrando pipeline.")
        return

    # 2. Garantir que a tabela existe
    create_table()

    # 3. Inserir os dados na tabela
    insert_data(data)

    logging.info("Pipeline finalizado com sucesso")

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(), # terminal
            logging.FileHandler("../logs/app.log", encoding="utf-8")  # arquivo
        ]
    )

    try:
        main()
    except Exception as e:
        logging.error(f"Erro fatal inesperado: {e}")