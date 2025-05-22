# mcpserver.py
import asyncio
import json
from typing import Any, Sequence
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from pydantic import BaseModel
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Import your custom SMTP connection function
from ReduceReuseRecycleGENAI import get_ser_conn

# Create server instance
server = Server("email-tool-server")

class EmailArguments(BaseModel):
    subject: str
    body: str
    receivers: str  # comma-separated email addresses

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="send_email",
            description="Send email via enterprise SMTP server",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string", 
                        "description": "Email body content (HTML supported)"
                    },
                    "receivers": {
                        "type": "string",
                        "description": "Comma-separated list of recipient email addresses"
                    }
                },
                "required": ["subject", "body", "receivers"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls"""
    if name != "send_email":
        raise ValueError(f"Unknown tool: {name}")
    
    if not arguments:
        raise ValueError("Missing arguments")
    
    try:
        # Validate arguments
        args = EmailArguments(**arguments)
        
        sender = "noreply-vkhvkm@company.com"  # Make sure this is valid
        recipients = [email.strip() for email in args.receivers.split(",")]
        
        # Create email message
        msg = MIMEMultipart()
        msg["Subject"] = args.subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(args.body, "html"))
        
        # SMTP connection
        smtpObj = get_ser_conn(
            logger=logger,
            env="preprod", 
            region_name="us-east-1",
            aplctn_cd="aedl",
            port=None,
            tls=True,
            debug=False
        )
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()
        
        logger.info(f"✅ Email sent successfully to: {', '.join(recipients)}")
        success_msg = f"✅ Email sent successfully to: {', '.join(recipients)}"
        
        return [types.TextContent(type="text", text=success_msg)]
        
    except Exception as e:
        error_msg = f"❌ Error sending email: {str(e)}"
        logger.error(error_msg)
        return [types.TextContent(type="text", text=error_msg)]

async def main():
    """Run the MCP server"""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="email-tool-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
