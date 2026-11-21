
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from mssql_python import connect
from pathlib import Path
from fastapi.responses import FileResponse

load_dotenv()

app = FastAPI(title="SQL API", version="1.1.0")


# -----------------------------
# Configuration
# -----------------------------

def get_connection():
    return connect(os.environ["SQL_CONNECTION_STRING"])


# -----------------------------
# Data models
# -----------------------------

class CustomerInput(BaseModel):
    FirstName: str = Field(min_length=1, max_length=100)
    LastName: str = Field(min_length=1, max_length=100)
    Email: str | None = Field(default=None, max_length=255)


def customer_to_dict(row):
    return {
        "CustomerId": row[0],
        "FirstName": row[1],
        "LastName": row[2],
        "Email": row[3],
    }


# -----------------------------
# Health check
# -----------------------------

@app.get("/")
def home():
    return {"message": "SQL API is running"}


# -----------------------------
# READ customers
# -----------------------------

@app.get("/api/customers")
def get_customers():

    with get_connection() as conn:
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

        return [
            customer_to_dict(row)
            for row in cursor.fetchall()
        ]


# -----------------------------
# CREATE customer
# -----------------------------

@app.post("/api/customers", status_code=201)
def create_customer(customer: CustomerInput):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO dbo.Customers (
                FirstName,
                LastName,
                Email
            )
            OUTPUT
                INSERTED.CustomerId,
                INSERTED.FirstName,
                INSERTED.LastName,
                INSERTED.Email
            VALUES (?, ?, ?)
        """, (
            customer.FirstName,
            customer.LastName,
            customer.Email,
        ))

        row = cursor.fetchone()
        result = customer_to_dict(row)

        conn.commit()

        return result


# -----------------------------
# UPDATE customer
# -----------------------------

@app.put("/api/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerInput):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE dbo.Customers
            SET
                FirstName = ?,
                LastName = ?,
                Email = ?
            OUTPUT
                INSERTED.CustomerId,
                INSERTED.FirstName,
                INSERTED.LastName,
                INSERTED.Email
            WHERE CustomerId = ?
        """, (
            customer.FirstName,
            customer.LastName,
            customer.Email,
            customer_id,
        ))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        result = customer_to_dict(row)

        conn.commit()

        return result


# -----------------------------
# DELETE customer
# -----------------------------

@app.delete(
    "/api/customers/{customer_id}",
    status_code=204
)
def delete_customer(customer_id: int):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM dbo.Customers
            OUTPUT DELETED.CustomerId
            WHERE CustomerId = ?
        """, (customer_id,))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        conn.commit()

    return Response(status_code=204)

# -----------------------------
# Frontend
# -----------------------------

@app.get("/app", include_in_schema=False)
def customer_app():
    html_file = Path(__file__).resolve().parent / "frontend" / "index.html"
    return FileResponse(html_file)