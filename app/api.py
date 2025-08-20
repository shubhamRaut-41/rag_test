import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
from .schemas import QueryRequest, QueryResponse
from .engine import RetrievalEngine

engine = RetrievalEngine()
app = FastAPI(title="Retrieval-Augmented Generation API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API. Visit /docs for API documentation."}

@app.post("/ingest")
def ingest_files(
    files: List[UploadFile] = File(...),
    replace: Optional[bool] = Form(False)
):
    try:
        result = engine.ingest(files, replace)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    try:
        result = engine.retrieve(req.question, req.k)

        return QueryResponse(
            answer=result.get("answer", "No answer found."),
            sources=result.get("sources", [])  # <-- always provide list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
def reset():
    try:
        return engine.reset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))