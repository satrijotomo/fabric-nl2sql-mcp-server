import json
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
    SCHEMA_CACHE_PATH
)

def load_schema():
    with open(SCHEMA_CACHE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def build_client():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )

    return AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_ad_token_provider=token_provider
    )

def generate_sql(question: str):
    schema_text = load_schema()
    client = build_client()

    system_prompt = f"""
You are a SQL generation service for Microsoft Fabric Lakehouse SQL endpoint.

Rules:
- Generate only read-only T-SQL.
- Allowed statements: SELECT or WITH...SELECT only.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, EXEC, MERGE.
- Prefer explicit column lists; avoid SELECT *.
- Use TOP for limiting rows where appropriate.
- If the question is ambiguous, choose the safest reasonable interpretation.
- Use only tables and columns from the schema below.

Schema:
{schema_text}
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        temperature=0,
        parallel_tool_calls=False,   # recommended with structured outputs per Microsoft doc
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "sql_plan",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "sql": {"type": "string"},
                        "reasoning": {"type": "string"},
                        "tables_used": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["sql", "reasoning", "tables_used"]
                }
            }
        },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    content = response.choices[0].message.content
    return json.loads(content)