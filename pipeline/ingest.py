"""
Chunks docs and tickets, embeds with sentence-transformers, upserts to Pinecone.
Run: python -m pipeline.ingest
"""
import json, os, time
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "all-MiniLM-L6-v2"
DIMENSION = 384
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "supportiq")


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 40) -> list[str]:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + chunk_size]))
        i += chunk_size - overlap
    return chunks


def ingest():
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    existing = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME not in existing:
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(2)

    index = pc.Index(INDEX_NAME)
    model = SentenceTransformer(EMBED_MODEL)

    data_path = Path(__file__).parent.parent / "data" / "mock_data.json"
    with open(data_path) as f:
        data = json.load(f)

    vectors = []

    for doc in data["docs"]:
        for i, chunk in enumerate(chunk_text(doc["content"])):
            vectors.append({
                "id": f"doc_{doc['id']}_chunk_{i}",
                "values": model.encode(chunk).tolist(),
                "metadata": {
                    "source_type": "doc",
                    "source_id": doc["id"],
                    "title": doc["title"],
                    "category": doc["category"],
                    "text": chunk,
                },
            })

    for ticket in data["tickets"]:
        text = f"Issue: {ticket['subject']}\n\nCustomer: {ticket['body']}\n\nResolution: {ticket['resolution']}"
        vectors.append({
            "id": f"ticket_{ticket['id']}",
            "values": model.encode(text).tolist(),
            "metadata": {
                "source_type": "ticket",
                "source_id": ticket["id"],
                "title": ticket["subject"],
                "category": ticket["category"],
                "tags": ", ".join(ticket.get("tags", [])),
                "text": text,
            },
        })

    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i : i + batch_size])

    print(f"Ingested {len(vectors)} vectors into '{INDEX_NAME}'")


if __name__ == "__main__":
    ingest()
