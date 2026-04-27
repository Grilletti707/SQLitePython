# SQLitePython

Pipeline de ingestão de dados CSV para SQLite com Python.

Lê um arquivo CSV de vendas, valida os dados e os insere em um banco SQLite local.

## Como rodar

**Pré-requisitos:** </br>
Python 3.10+ </br>
pip </br>

**Recomendações opcionais**
SQLite Viewer - Visualizar arquivos .db para VS Code </br>
Utilizar venv (Altamente recomendado) </br>

1. Clone o repositório: </br>
````bash
git clone https://github.com/Grilletti707/SQLitePython.git
cd SQLitePython
````

2. Inicialize o venv no seu ambiente: </br>
```bash
python -m venv venv
venv\Scripts\activate
```

3. Baixe os requerimentos para rodar a API: </br>
```bash
pip install -r requirements.txt
```

4. Execute o pipeline </br>
```bash
python -m src.main
```

5. Para subir a API, utilize: </br>
```bash
uvicorn main:app --reload
```
Ou
```bash
python -m uvicorn src.main:app --reload
```

O banco será criado automaticamente em `db/database.db`.

## Estrutura

| Pasta      | Função                        |
|------------|-------------------------------|
| `data/`    | Arquivos CSV de entrada       |
| `db/`      | Banco SQLite gerado           |
| `logs/`    | Logs de execução              |
| `src/`     | Código fonte                  |

## Próximos passos

- [ ] API REST com FastAPI para consulta dos dados
