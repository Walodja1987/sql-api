import os
from fastapi import FastAPI
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()

app = FastAPI(title="SQL API")


@app.get("/")
def home():
    return {"message": "SQL API is running"}


@app.get("/api/customers")
def get_customers():

    connection_string = os.environ["SQL_CONNECTION_STRING"]

    with connect(connection_string) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                CustomerId,
                FirstName,
                LastName,
                Email
            FROM dbo.Customers
            ORDER BY CustomerId
        """)

        rows = cursor.fetchall()

        return [
            {
                "CustomerId": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "Email": row[3]
            }
            for row in rows
        ]