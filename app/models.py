from pydantic import BaseModel, Field
from typing import List, Optional, Any

class AskRequest(BaseModel):
    question: str = Field(..., description="Natural language question from the user")

class SqlPlan(BaseModel):
    sql: str
    reasoning: str
    tables_used: List[str]
    parameters: Optional[dict] = None

class QueryResponse(BaseModel):
    success: bool
    sql: Optional[str] = None
    rows: Optional[list] = None
    error: Optional[str] = None