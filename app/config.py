import os

FABRIC_SQL_SERVER = os.getenv("FABRIC_SQL_SERVER")   # e.g. yourworkspace.datawarehouse.fabric.microsoft.com
FABRIC_DATABASE = os.getenv("FABRIC_DATABASE")       # e.g. your lakehouse SQL endpoint database
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. gpt-4.1
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
SCHEMA_CACHE_PATH = os.getenv("SCHEMA_CACHE_PATH", "schema.txt")
MAX_ROWS = int(os.getenv("MAX_ROWS", "200"))