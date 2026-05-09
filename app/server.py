from fastapi import FastAPI, HTTPException
from models import AskRequest, QueryResponse
from nl2sql import generate_sql
from sql_guard import validate_sql, enforce_row_limit
from fabric_sql import run_sql

app = FastAPI(title="Fabric Lakehouse NL2SQL MCP Wrapper")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tools/query_lakehouse", response_model=QueryResponse)
def query_lakehouse(req: AskRequest):
    try:
        plan = generate_sql(req.question)

        sql = plan["sql"]
        validate_sql(sql)
        sql = enforce_row_limit(sql, max_rows=200)

        rows = run_sql(sql)

        return QueryResponse(
            success=True,
            sql=sql,
            rows=rows
        )

    except Exception as e:
        return QueryResponse(
            success=False,
            error=str(e)
        )