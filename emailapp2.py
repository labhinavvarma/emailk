# app.py

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from mcpserver import mcp
from router import route

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup SSE transport
sse = SseServerTransport("/messages")
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/messages", tags=["MCP"], include_in_schema=True)
def messages_docs(session_id: str):
    """SSE endpoint doc entry (no-op)"""
    pass

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )

# Register custom router for MCP tool invocation
app.include_router(route)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
