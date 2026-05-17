from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import json, sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.generate import query as rag_query

app = FastAPI(title="SupportIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = Path(__file__).parent.parent / "web"
app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/")
def serve_ui():
    return FileResponse(str(web_dir / "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/articles")
def list_docs():
    data_path = Path(__file__).parent.parent / "data" / "mock_data.json"
    with open(data_path) as f:
        data = json.load(f)
    return [
        {
            "id": doc["id"],
            "title": doc["title"],
            "category": doc["category"],
            "preview": doc["content"][:200].rsplit(" ", 1)[0] + "...",
            "content": doc["content"],
        }
        for doc in data["docs"]
    ]


@app.post("/query")
def query_endpoint(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")
    return rag_query(req.query, top_k=req.top_k)
