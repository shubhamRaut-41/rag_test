from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    files: List[str]
    replace: Optional[bool] = False

class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]