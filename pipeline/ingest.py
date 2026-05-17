import json, os, time
from pathlib import Path
import voyageai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

DIMENSION = 512
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
    vo = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])

    existing = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME in existing:
        pc.delete_index(INDEX_NAME)
        print(f"Deleted existing index '{INDEX_NAME}'")

    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(INDEX_NAME).status["ready"]:
        time.sleep(2)
    print(f"Created index '{INDEX_NAME}' ({DIMENSION}d)")

    index = pc.Index(INDEX_NAME)

    data_path = Path(__file__).parent.parent / "data" / "mock_data.json"
    with open(data_path) as f:
        data = json.load(f)

    records = []

    for doc in data["docs"]:
        for i, chunk in enumerate(chunk_text(doc["content"])):
            records.append({
                "id": f"doc_{doc['id']}_chunk_{i}",
                "text": chunk,
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
        records.append({
            "id": f"ticket_{ticket['id']}",
            "text": text,
            "metadata": {
                "source_type": "ticket",
                "source_id": ticket["id"],
                "title": ticket["subject"],
                "category": ticket["category"],
                "tags": ", ".join(ticket.get("tags", [])),
                "text": text,
            },
        })

    batch_size = 10
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        texts = [r["text"] for r in batch]
        result = vo.embed(texts, model="voyage-3-lite", input_type="document")
        vectors = [
            {"id": r["id"], "values": emb, "metadata": r["metadata"]}
            for r, emb in zip(batch, result.embeddings)
        ]
        index.upsert(vectors=vectors)
        print(f"Upserted {i + len(batch)}/{len(records)}")
        if i + batch_size < len(records):
            time.sleep(21)

    print(f"Ingested {len(records)} vectors into '{INDEX_NAME}'")


if __name__ == "__main__":
    ingest()
