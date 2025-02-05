# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import Optional

import uvicorn

from agent import SQLiteAgent

class QueryRequest(BaseModel):
    query: str
    model_name: Optional[str] = "deepseek-r1:8b"
    db_path: Optional[str] = "products.db"

class QueryResponse(BaseModel):
    result: str
    error: Optional[str] = None

app = FastAPI(title="SQLite AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        agent = SQLiteAgent(request.db_path, model_name=request.model_name)
        result = agent.run(request.query)
        return QueryResponse(result=str(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_fastapi()