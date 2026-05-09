# ✅ ✅ architecture.md

```markdown
# Architecture Overview

## 1. Problem

Fabric Data Agents require **delegated user identity**, but:

- Teams / M365 → uses App identity
- Direct integration fails

---

## 2. Solution

Introduce a **middleware MCP server**

---

## 3. Data flow


User query
↓
MCP server receives request
↓
LLM generates SQL (structured output)
↓
SQL validated (guardrails)
↓
SQL executed on Fabric
↓
Results returned

---

## 4. Components

### MCP Server
- FastAPI service
- Exposes tool endpoints

### NL2SQL Engine
- Azure OpenAI / Foundry model
- Generates SQL using schema context

### SQL Guard
- Prevents destructive queries
- Enforces read-only access

### Fabric Execution Layer
- SQL endpoint via ODBC
- Managed Identity authentication

---

## 5. Security design

- No write operations allowed
- Controlled schema exposure
- Row limit enforcement
- No dynamic table injection

---

## 6. Why not Fabric Data Agent directly

- API not fully GA
- Identity mismatch
- Limited runtime support

---

## 7. Why MCP

- Standardized tool interface
- Multi-agent ready
- Works with Foundry & Copilot

---

## 8. Extensibility

You can add:

- More tools (KPI, schema explorer, etc.)
- Semantic layer
- Business logic layer

---