import asyncio
from fastmcp import Client
from fastmcp.exceptions import ClientError:contentReference[oaicite:2]{index=2}

:contentReference[oaicite:4]{index=4}
    :contentReference[oaicite:5]{index=5}
    :contentReference[oaicite:6]{index=6}

    # Initialize the MCP client
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

        except ClientError as e:
            print(f"❌ Tool call failed: {e}")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")

:contentReference[oaicite:8]{index=8}
    :contentReference[oaicite:9]{index=9}
