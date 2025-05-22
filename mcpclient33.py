import asyncio
from fastmcp import Client

async def main():
    # Replace with your MCP server's URL
    server_url = "http://<MCP_SERVER_PUBLIC_IP>:8000"
    client = Client(server_url)

    async with client:
        # Invoke the send_email tool
        result = await client.call_tool("send_email", {
            "subject": "Test Email",
            "body": "<p>This is a test email sent via MCP.</p>",
            "receivers": "recipient@example.com"
        })
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
