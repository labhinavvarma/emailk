from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
from pydantic import BaseModel
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ReduceReuseRecycleGENAI import get_ser_conn
from typing import Dict

# Initialize MCP server
mcp = FastMCP("Email Tool MCP Server")

# Email sending arguments schema
class EmailArguments(BaseModel):
    subject: str
    body: str
    receivers: str  # comma-separated emails

# MCP Tool definition
@mcp.tool(name="mcp-send-email", description="Send email to one or more recipients via Outlook SMTP")
async def send_email_tool(args: EmailArguments) -> Message:
    try:
        sender = 'noreply-vkhvkm@yourdomain.com'  # change to a valid sender
        subject = args.subject
        body = args.body
        receivers = args.receivers

        recipients = [email.strip() for email in receivers.split(",")]

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(body, 'html'))

        smtpObj = get_ser_conn(logger, env="preprod", region_name="us-east-1", aplctn_cd="aedl", port=None, tls=True, debug=False)
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()

        return Message.text(f"✅ Email sent to: {', '.join(recipients)}")

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return Message.text(f"❌ Failed to send email: {e}")

# Run MCP FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
