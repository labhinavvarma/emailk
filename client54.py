import asyncio
from mcp import ClientSession
from mcp.types import TextContent

SERVER_URL = "http://localhost:8000"  # 🔁 or your EC2 IP

TOOL_NAME = "mcp-send-email"
INPUT = {
    "subject": "📨 MCP SDK Client Test",
    "body": "<p>This is a test from SDK-based client.</p>",
    "receivers": "test@example.com"
}

async def main():
    async with ClientSession(server_url=SERVER_URL) as session:
        # ✅ This is the official way to call tools
        result = await session.invoke_tool(TOOL_NAME, INPUT)

        if isinstance(result.content, TextContent):
            print("✅ Result Text:", result.content.text)
        else:
            print("✅ Non-text result:", result)

if __name__ == "__main__":
    asyncio.run(main())
