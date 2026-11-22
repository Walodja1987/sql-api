# SQL API

FastAPI CRUD API for SQL Server `dbo.Customers`, plus a simple frontend.

Full home-lab walkthrough (SQL Server, SSMS, WSL, migrations): [SQL Server guide](https://walodja1987.github.io/sql-api/guide/sql_server_guide.html)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn python-dotenv mssql-python
```

Create a `.env` in the project root:

```env
SQL_CONNECTION_STRING="Server=<HOST>,1433;Database=TestDB;UID=sqlapi;PWD=<PASSWORD>;Encrypt=yes;TrustServerCertificate=yes;"
```

Apply the SQL scripts in `migrations/` (in order) before starting the API.

## Run

```bash
source .venv/bin/activate
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

- API docs: http://127.0.0.1:8000/docs
- Frontend: http://127.0.0.1:8000/app