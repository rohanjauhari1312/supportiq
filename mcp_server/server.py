"""
SupportIQ MCP server — stdio transport.

Usage:
  python -m mcp_server.server

Add to Claude Code MCP config:
  {
    "mcpServers": {
      "supportiq": {
        "command": "python",
        "args": ["-m", "mcp_server.server"],
        "cwd": "/path/to/SupportIQ"
      }
    }
  }
"""
import asyncio, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pipeline.generate import query as rag_query

app = Server("supportiq")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_knowledge_base",
            description=(
                "Search SupportIQ's internal knowledge base of docs and past tickets. "
                "Returns a grounded answer with cited sources. Use this to answer support "
                "questions without leaving your current workflow."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The support question to look up.",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of source chunks to retrieve (default 5).",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "query_knowledge_base":
        raise ValueError(f"Unknown tool: {name}")
    result = rag_query(arguments["query"], top_k=arguments.get("top_k", 5))
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
