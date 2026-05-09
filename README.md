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

