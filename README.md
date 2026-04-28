# SQLitePython

## Overview

A Python-based data pipeline that ingests sales data from CSV files, validates it, stores it in a local SQLite database, and exposes it through a REST API built with FastAPI.

## Tech Stack

- Python
- FastAPI
- SQLite
- Pydantic

## Getting started

**Prerequisites:** </br>
Python 3.10+ </br>
pip </br>

**Optional:** </br>
- SQLite Viewer (VS Code extension) – for inspecting `.db` files

1. Clone the repo: </br>
````bash
git clone https://github.com/Grilletti707/SQLitePython.git
cd SQLitePython
````

2. Create and activate a virtual environment: </br>
```bash
python -m venv venv
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

3. Install dependencies: </br>
```bash
pip install -r requirements.txt
```

4. Run the data ingestion pipeline: </br>
```bash
python -m src.main
```

5. To run the API, use: </br>
```bash
python -m uvicorn src.main:app --reload
```

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/sales" \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "cliente": "Lucca",
  "produto": "Notebook",
  "valor": 3500.0,
  "data": "2026-04-27"
}'
```

The database will be automatically created in `db/database.db`.

## Structure

| Folder     | Description                   |
|------------|-------------------------------|
| `data/`    | CSV data input                |
| `db/`      | SQLite database storage       |
| `logs/`    | Application logs              |
| `src/`     | Application source code       |

## API Endpoints

| Method | Endpoint             | Description                           |
|--------|----------------------|---------------------------------------|
| POST   | /sales               | Create a new sale                     |
| GET    | /sales               | List sales with optional filters      |
| GET    | /sales/{id}          | Get a sale by ID                      |
| DELETE | /sales/{id}          | Delete a sale by ID                   |
| GET    | /sales/report        | Get aggregated sales report           |
| POST   | /sales/import        | Upload a CSV file and insert records  |

## Roadmap

- [x] REST API with FastAPI
- [x] Filtering and pagination
- [ ] Update (PUT/PATCH) endpoint
- [ ] Improved error handling
- [ ] Token-based authentication (JWT)