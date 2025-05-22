# mcpclient.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_email_tool():
    """Test the email MCP server"""
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["mcpserver.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test the email tool
            print("\nTesting email tool...")
            try:
                result = await session.call_tool(
                    "send_email",
                    {
                        "subject": "Test Email from MCP",
                        "body": "<h1>Hello!</h1><p>This is a test email sent via MCP server.</p>",
                        "receivers": "test@example.com, another@example.com"
                    }
                )
                
                print("Email tool result:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(f"  {content.text}")
                    else:
                        print(f"  {content}")
                        
            except Exception as e:
                print(f"Error calling email tool: {e}")

async def interactive_client():
    """Interactive MCP client for testing"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcpserver.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("MCP Email Client - Interactive Mode")
            print("Commands: 'list' (list tools), 'send' (send email), 'quit' (exit)")
            
            while True:
                try:
                    command = input("\n> ").strip().lower()
                    
                    if command == "quit":
                        break
                        
                    elif command == "list":
                        tools = await session.list_tools()
                        print("Available tools:")
                        for tool in tools.tools:
                            print(f"  - {tool.name}: {tool.description}")
                            
                    elif command == "send":
                        subject = input("Subject: ")
                        body = input("Body (HTML): ")
                        receivers = input("Recipients (comma-separated): ")
                        
                        try:
                            result = await session.call_tool(
                                "send_email",
                                {
                                    "subject": subject,
                                    "body": body,
                                    "receivers": receivers
                                }
                            )
                            
                            print("Result:")
                            for content in result.content:
                                if hasattr(content, 'text'):
                                    print(f"  {content.text}")
                                else:
                                    print(f"  {content}")
                                    
                        except Exception as e:
                            print(f"Error: {e}")
                            
                    else:
                        print("Unknown command. Use 'list', 'send', or 'quit'")
                        
                except KeyboardInterrupt:
                    break
            
            print("\nGoodbye!")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Test mode (automated test)")
    print("2. Interactive mode")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(test_email_tool())
    else:
        asyncio.run(interactive_client())
