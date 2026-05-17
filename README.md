# SupportIQ

A RAG pipeline for support teams. Index your internal docs and past tickets, then query them from a web UI, the FastAPI, or directly inside Claude Code via an MCP tool. Answers are grounded in retrieved content and cite sources inline.

## Architecture

```
User / Claude Code
       |
       | (MCP stdio OR HTTP POST /query)
       v
  +-----------+        +------------------+
  | MCP Server|        |  FastAPI (api/)   |
  |  (stdio)  |        |  serves web UI   |
  +-----------+        +------------------+
       |                        |
       +----------+-------------+
                  |
            pipeline/generate.py
                  |
       +----------+-------------+
       |                        |
  pipeline/retrieve.py    Anthropic API
  (sentence-transformers   (claude-sonnet-4-6)
   + Pinecone query)
       |
  Pinecone Index
  (embedded by pipeline/ingest.py)
       |
  data/mock_data.json
  (15 docs + 60 tickets)
```

## Setup

### 1. Environment variables

```bash
cp .env.example .env
# Fill in ANTHROPIC_API_KEY, PINECONE_API_KEY, and optionally PINECONE_INDEX_NAME
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Ingest data

Run once (or whenever mock_data.json changes). Creates the Pinecone index if it does not exist, embeds all docs and tickets, and upserts them.

```bash
python -m pipeline.ingest
```

### 4. Run the API + web UI

```bash
uvicorn api.app:app --reload --port 8000
```

Open http://localhost:8000 in a browser. Type a question and press Enter or click Ask.

### 5. Run the MCP server (standalone)

```bash
python -m mcp_server.server
```

The server speaks the MCP stdio protocol. See the MCP integration section below.

## MCP integration

Add SupportIQ as an MCP server in your Claude Code config (`~/.claude/mcp_config.json` or the project-level equivalent):

```json
{
  "mcpServers": {
    "supportiq": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/SupportIQ",
      "env": {
        "ANTHROPIC_API_KEY": "sk-...",
        "PINECONE_API_KEY": "...",
        "PINECONE_INDEX_NAME": "supportiq"
      }
    }
  }
}
```

After restarting Claude Code, the tool `query_knowledge_base` is available in your session. Call it with a `query` string and an optional `top_k` integer (default 5).

## Running the eval harness

```bash
# Basic run (prints per-case metrics + summary to stdout)
python -m eval.run_eval

# Custom top-k and save results
python -m eval.run_eval --top-k 8 --output eval/results.json
```

Metrics reported:
- **Precision@k** — fraction of retrieved chunks whose source ID matches an expected source
- **Recall@k** — fraction of expected sources found in the top-k results
- **Keyword hit rate** — fraction of expected keywords present in the generated answer
- **Mean latency** — end-to-end ms including retrieval and generation

## Key design decisions

**Chunking strategy**: Docs are split into 400-word chunks with 40-word overlap. Overlap prevents a sentence from being cut at a boundary where its meaning depends on the preceding context. Tickets are kept as single vectors (subject + body + resolution concatenated) because they are short and splitting them would lose the cause-effect relationship.

**Embedding model**: `all-MiniLM-L6-v2` (384 dimensions). It is small enough to run locally without a GPU, loads in under two seconds on first call, and performs well on sentence-level semantic similarity. For production with higher query volume, swapping to a larger model is straightforward — only `EMBED_MODEL` and `DIMENSION` in ingest.py and retrieve.py need to change.

**Citation format**: The system prompt instructs the model to cite sources using `[Source N]` inline and list them in a Sources section at the end. The source list is assembled from the retrieved chunks before the API call, so the model can reference them by index rather than needing to reproduce full titles in the answer body.

**Pinecone serverless**: The ingest script defaults to the AWS us-east-1 serverless spec, which has no idle cost and scales to zero when not in use. The index name is configurable via `PINECONE_INDEX_NAME` to avoid collisions in shared accounts.
