from pydantic import BaseModel
from typing import List, Dict, Any

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    summary: str
