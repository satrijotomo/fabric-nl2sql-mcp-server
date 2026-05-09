import re

FORBIDDEN = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bMERGE\b",
    r"\bEXEC\b",
    r"\bCREATE\b",
    r";",  # optional: reject multi-statement
]

ALLOWED_PREFIXES = [
    "SELECT",
    "WITH"
]

def validate_sql(sql: str):
    if not sql or not sql.strip():
        raise ValueError("Generated SQL is empty.")

    upper_sql = sql.strip().upper()

    if not any(upper_sql.startswith(p) for p in ALLOWED_PREFIXES):
        raise ValueError("Only read-only SELECT/CTE queries are allowed.")

    for pattern in FORBIDDEN:
        if re.search(pattern, upper_sql, flags=re.IGNORECASE):
            raise ValueError(f"Forbidden SQL pattern detected: {pattern}")

    return True


def enforce_row_limit(sql: str, max_rows: int = 200):
    upper_sql = sql.upper()
    if "TOP " in upper_sql:
        return sql

    if upper_sql.startswith("SELECT"):
        return re.sub(r"^\s*SELECT\s+", f"SELECT TOP {max_rows} ", sql, count=1, flags=re.IGNORECASE)

    return sql