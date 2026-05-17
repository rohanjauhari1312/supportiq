import os
from pathlib import Path
import voyageai
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "supportiq")

_voyage: voyageai.Client | None = None
_index = None


def _get_voyage() -> voyageai.Client:
    global _voyage
    if _voyage is None:
        _voyage = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
    return _voyage


def _get_index():
    global _index
    if _index is None:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        _index = pc.Index(INDEX_NAME)
    return _index


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    result = _get_voyage().embed([query], model="voyage-3-lite", input_type="query")
    embedding = result.embeddings[0]
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
