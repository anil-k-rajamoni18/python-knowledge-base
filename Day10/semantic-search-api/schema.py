from pydantic import BaseModel
from typing import Any, List, Dict

class DocumentAddRequest(BaseModel):
    text: str
    metadata: dict

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    results: List[Dict[str, Any]]
