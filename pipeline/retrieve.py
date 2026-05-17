import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "supportiq")

_model: SentenceTransformer | None = None
_index = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def _get_index():
    global _index
    if _index is None:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _index = pc.Index(INDEX_NAME)
    return _index


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    embedding = _get_model().encode(query).tolist()
    results = _get_index().query(vector=embedding, top_k=top_k, include_metadata=True)
    return [
        {
            "id": m.id,
            "score": round(m.score, 4),
            "source_type": m.metadata.get("source_type"),
            "source_id": m.metadata.get("source_id"),
            "title": m.metadata.get("title"),
            "category": m.metadata.get("category", ""),
            "text": m.metadata.get("text", ""),
        }
        for m in results.matches
    ]
