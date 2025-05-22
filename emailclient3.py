import asyncio
from mcp import ClientSession
from mcp.types import TextContent

# Your MCP server base URL (change this to your EC2 IP if needed)
MCP_SERVER_URL = "http://localhost:8000"

# Tool name and input
TOOL_NAME = "mcp-send-email"
TOOL_INPUT = {
    "subject": "✅ Alternate MCP Client",
    "body": "<p>This email was sent using the official MCP ClientSession.</p>",
    "receivers": "you@example.com"
}

async def run_tool():
    async with ClientSession(server_url=MCP_SERVER_URL) as session:
        result = await session.invoke_tool(TOOL_NAME, TOOL_INPUT)
        if isinstance(result.content, TextContent):
            print("✅ Tool Output:")
            print(result.content.text)
        else:
            print("✅ Tool ran, non-text output:", result)

# Run the client
if __name__ == "__main__":
    asyncio.run(run_tool())
