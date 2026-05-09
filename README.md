# Fabric Lakehouse NL → SQL MCP Server

This repository provides a **Model Context Protocol (MCP)-compatible server** that enables:

✅ Natural language queries  
✅ Automated SQL generation using Azure OpenAI / Foundry  
✅ Secure execution against Microsoft Fabric Lakehouse SQL endpoint  
✅ Safe, read-only analytics access  

---

## 🚀 What problem this solves

Microsoft Fabric Data Agents currently have:
- Limited external REST support
- Identity mismatch issues when used with Teams / M365 agents

This project provides a **wrapper pattern** that:

✅ Works reliably with Teams + Foundry  
✅ Uses Managed Identity for Fabric access  
✅ Adds safety + observability  
✅ Supports multi-agent orchestration  

---

## 🧠 Architecture Overview
User (Teams / Copilot)

↓

Foundry Agent

↓

MCP Server (this repo)

↓

NL → SQL (Azure OpenAI)

↓

SQL Guard (validation + safety)

↓

Fabric SQL Endpoint (Lakehouse)

↓

JSON response

👉 See ./architecture.md for details.

---

## ⚙️ Features

- Natural language to SQL generation
- Structured output (JSON schema enforced)
- SQL safety validation (read-only enforcement)
- Row limiting (`TOP N`)
- Fabric Lakehouse integration
- MCP-compatible tool endpoint

---

## 📦 Setup

### 1. Clone repo


git clone https://github.com/<your-org>/fabric-nl2sql-mcp-server.git


### 2. Install dependencies

pip install -r requirements.txt

### 3. Configure environment

cp .env.example .env

Fill values:

FABRIC_SQL_SERVER=<your-server>.datawarehouse.fabric.microsoft.com
FABRIC_DATABASE=<your-db>

AZURE_OPENAI_ENDPOINT=https://<your-openai>.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4.1

### 4. Run locally

uvicorn app.server:app --reload --port 7071


### Example request

POST /tools/query_lakehouse
{
  "question": "What are the top 10 customers by revenue this year?"
}

### Example response

{
  "success": true,
  "sql": "SELECT TOP 10 c.customer_name, SUM(oi.line_amount) AS revenue ...",
  "rows": [
    { "customer_name": "Contoso", "revenue": 154230.25 }
  ]
}

🧪 Usage in Foundry / Agents
Add tool:
https://<your-app>/tools/query_lakehouse

Schema:

{
  "type": "object",
  "properties": {
    "question": { "type": "string" }
  },
  "required": ["question"]
}
``

### Test:
1. Run from project root folder: 
uvicorn app.server:app --reload --port 7071

2. Open http://127.0.0.1:7071/docs

3. Test the POST /tools/query_lakehouse


Here’s a clean **single block you can paste directly into your README** 👍  
It merges everything we discussed into a concise, practical section.

***

## 🔄 Switching to a Different Lakehouse / Database

This project is designed to be reusable across different Microsoft Fabric Lakehouses. When onboarding a new dataset, you only need to update a few configuration files—everything else remains reusable.

***

### ✅ Required Changes

#### 1. Update Connection Settings (`.env`)

Modify the Fabric connection details:

```env
FABRIC_SQL_SERVER=<your-sql-endpoint>
FABRIC_DATABASE=<your-database-name>
```

*   `FABRIC_SQL_SERVER`: Use the SQL endpoint host from Fabric (usually a long GUID-like string).
*   `FABRIC_DATABASE`: Use the SQL endpoint database name (often matches the Lakehouse name).

***

#### 2. Update Semantic Schema (`app/schema.txt`) ⭐ *Most Important*

This file defines how the LLM understands your data model.

You must update:

*   ✅ Table names
*   ✅ Key columns
*   ✅ Relationships
*   ✅ Business meaning

Example:

```txt
Tables:
dbo.orders
dbo.customers
dbo.products

Relationships:
orders.customer_id = customers.id
orders.product_id = products.id

Business meaning:
- Customers place orders
- Each order is associated with a product

Rules:
- Always use dbo schema
- Only use listed tables
- Prefer JOINs when relationships exist
- Do not use sys tables
```

👉 If this file is outdated or incorrect:

*   SQL generation will be inaccurate
*   Joins may fail
*   The model may hallucinate tables

***

### ⚠️ Conditional Changes

#### 3. Adjust Schema Name (`app/fabric_sql.py`)

If your Lakehouse uses a schema other than `dbo`, update:

```sql
AND TABLE_SCHEMA = 'dbo'
```

to:

```sql
AND TABLE_SCHEMA = '<your_schema>'
```

***

### ✅ No Changes Needed

The following files are reusable across datasets:

*   `app/server.py` → API + orchestration logic
*   `app/nl2sql.py` → LLM prompt and SQL generation
*   `app/sql_guard.py` → SQL safety and validation

These components are dataset‑agnostic.

***

### 💡 Recommended Structure for Multi-Dataset Use

Instead of editing `schema.txt` each time, create separate schema files:

    schemas/
      banking_schema.txt
      retail_schema.txt
      healthcare_schema.txt

Then update `.env`:

```env
SCHEMA_FILE=schemas/<your_schema>.txt
```

And in `config.py`:

```python
SCHEMA_FILE = os.getenv("SCHEMA_FILE", "app/schema.txt")
```

👉 This allows you to switch datasets without modifying code.

***

### 🚀 Optional Enhancement (Advanced)

For production scenarios, you can dynamically generate schema metadata:

```sql
SELECT TABLE_NAME, COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
```

and inject it into the prompt instead of maintaining `schema.txt` manually.

***

### ✅ Summary

When switching Lakehouses:

| File            | Change Required  | Notes                                 |
| --------------- | ---------------- | ------------------------------------- |
| `.env`          | ✅ Yes            | Update server + database              |
| `schema.txt`    | ✅ Yes (critical) | Update tables, columns, relationships |
| `fabric_sql.py` | ⚠️ Sometimes     | Update schema name if needed          |
| `server.py`     | ❌ No             | Fully reusable                        |
| `nl2sql.py`     | ❌ No             | Reusable (prompt can be tuned)        |
| `sql_guard.py`  | ❌ No             | Reusable                              |

***

### 🧠 Key Principle

The system is **schema-driven**:

    LLM + schema.txt → SQL → Fabric → Results

👉 The quality of responses depends heavily on schema.txt.
Include relationships and business meaning to enable accurate analytics queries.

***



