import pyodbc
from app.config import FABRIC_SQL_SERVER, FABRIC_DATABASE

def run_sql(sql: str):
    conn = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{FABRIC_SQL_SERVER},1433;"
        f"Database={FABRIC_DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
        "Authentication=ActiveDirectoryInteractive"
    )

    cursor = conn.cursor()
    cursor.execute(sql)

    columns = [c[0] for c in cursor.description]
    rows = cursor.fetchall()

    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()
    return result