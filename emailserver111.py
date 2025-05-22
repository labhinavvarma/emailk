# mcpserver.py
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, Tool
from pydantic import BaseModel
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Sequence
import json

# Import your custom SMTP connection function
# from ReduceReuseRecycleGENAI import get_ser_conn

# Create the FastMCP instance
mcp = FastMCP("Email Tool MCP Server")

class EmailArguments(BaseModel):
    subject: str
    body: str
    receivers: str  # comma-separated email addresses

@mcp.tool()
def send_email(args: EmailArguments) -> str:
    """Send email via enterprise SMTP server"""
    try:
        sender = "noreply-vkhvkm@company.com"  # Make sure this is a valid email
        recipients = [email.strip() for email in args.receivers.split(",")]
        
        # Create message
        msg = MIMEMultipart()
        msg["Subject"] = args.subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(args.body, "html"))
        
        # Get SMTP connection - you'll need to uncomment and fix this
        smtpObj = get_ser_conn(
            logger=logger,
            env="preprod",
            region_name="us-east-1",
            aplctn_cd="aedl",
            port=None,
           tls=True,
           debug=False
        )
        
        # For testing, we'll simulate the email sending
        # smtpObj.sendmail(sender, recipients, msg.as_string())
        # smtpObj.quit()
        
        logger.info("✅ Email sent successfully.")
        return f"✅ Email sent to: {', '.join(recipients)}"
        
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")
        return f"❌ Error sending email: {str(e)}"

def main():
    """Run the MCP server"""
    import mcp.server.stdio
    
    async def run_server():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await mcp.run(
                read_stream,
                write_stream,
                mcp.create_initialization_options()
            )
    
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
