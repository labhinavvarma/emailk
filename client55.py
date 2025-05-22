import asyncio
from fastmcp import Client

async def main():
    # Replace with your MCP server's URL
    mcp_server_url = "http://<MCP_SERVER_IP>:8000/mcp"

    client = Client(mcp_server_url)

    async with client:
        try:
            # Optional: Ping the server to verify connectivity
            await client.ping()
            print("✅ Connected to MCP server.")

            # Optional: List available tools
            tools = await client.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")

            # Define email parameters
            email_params = {
                "subject": "Test Email from MCP Client",
                "body": "<p>This is a test email sent via MCP.</p>",
                "receivers": "recipient@example.com"
            }

            # Invoke the send_email tool
            result = await client.call_tool("send_email", email_params)
            print(f"📧 Email send result: {result}")

            # Invoke the compose_email_prompt prompt
            prompt_response = await client.call_prompt("compose_email_prompt", email_params)
            print(f"📝 Prompt response: {prompt_response.text}")

        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
