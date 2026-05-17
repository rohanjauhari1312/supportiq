import os, time
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from .retrieve import retrieve

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

MODEL = "claude-sonnet-4-6"
_client: anthropic.Anthropic | None = None

SYSTEM = """You are SupportIQ, an internal knowledge assistant for support teams.

Answer questions using ONLY the provided context. If the context is insufficient, say so clearly — do not guess.

Cite sources inline using [Source N] notation. End your response with a "Sources" section listing each cited source."""


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def query(question: str, top_k: int = 5) -> dict:
    t0 = time.perf_counter()
    chunks = retrieve(question, top_k=top_k)

    if not chunks:
        return {
            "answer": "No relevant content found in the knowledge base for this query.",
            "sources": [],
            "latency_ms": round((time.perf_counter() - t0) * 1000),
            "chunks_retrieved": 0,
        }

    context = "\n\n---\n\n".join(
        f"[Source {i}] {c['title']} ({c['source_type']})\n{c['text']}"
        for i, c in enumerate(chunks, 1)
    )

    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
    )

    return {
        "answer": response.content[0].text,
        "sources": [
            {
                "index": i,
                "title": c["title"],
                "source_type": c["source_type"],
                "score": c["score"],
                "category": c["category"],
            }
            for i, c in enumerate(chunks, 1)
        ],
        "latency_ms": round((time.perf_counter() - t0) * 1000),
        "chunks_retrieved": len(chunks),
    }
