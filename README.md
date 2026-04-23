# SQLitePython

Pipeline de ingestão de dados CSV para SQLite com Python.

Lê um arquivo CSV de vendas, valida os dados e os insere em um banco SQLite local.

## Como rodar

**Pré-requisitos:** Python 3.10+

Sem dependências externas. Todas as bibliotecas usadas são da biblioteca padrão do Python.

1. Clone o repositório
git clone https://github.com/Grilletti707/SQLitePython.git
cd SQLitePython

2. Execute o pipeline

python src/main.py

O banco será criado automaticamente em `db/database.db`.

## Estrutura
data/       CSV de entrada
db/         Banco SQLite gerado
logs/       Logs de execução
src/        Código fonte

## Próximos passos

- [ ] API REST com FastAPI para consulta dos dados