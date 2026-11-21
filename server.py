from fastapi import FastAPI
from mssql_python import connect

app = FastAPI()

CONNECTION_STRING = (
    "Server=localhost\\SQLEXPRESS;"
    "Database=TestDB;"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)


@app.get("/api/customers")
def get_customers():

    with connect(CONNECTION_STRING) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                CustomerId,
                FirstName,
                LastName,
                Email
            FROM Customers
            ORDER BY CustomerId
        """)

        rows = cursor.fetchall()

        customers = []

        for row in rows:
            customers.append({
                "CustomerId": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "Email": row[3]
            })

        return customers