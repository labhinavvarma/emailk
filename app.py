import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from router import route
from mcpserver import mcp

app = mcp.app  # Use the MCP FastAPI app instance

# Allow all CORS for testing (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup SSE route
sse = SseServerTransport("/messages")
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/messages", tags=["MCP"], include_in_schema=True)
def messages_docs(session_id: str):
    """For docs only. Real handler is mounted."""
    pass

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request):
    """MCP SSE endpoint"""
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )

# Include tool/email routes
app.include_router(route)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
