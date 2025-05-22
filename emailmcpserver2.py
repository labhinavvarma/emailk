# mcpserver.py

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from loguru import logger
from ReduceReuseRecycleGENAI import get_ser_conn

mcp = FastMCP("MCP Email Tool Server")

env = "preprod"
region_nm = "us-east-1"

class EmailArguments(BaseModel):
    subject: str
    body: str
    receivers: str

@mcp.tool(name="mcp-send-email", description="Send email using enterprise SMTP")
async def send_email_tool(args: EmailArguments) -> Message:
    try:
        sender = 'noreply-vkhvkm'
        recipients = [email.strip() for email in args.receivers.split(",")]

        msg = MIMEMultipart()
        msg['Subject'] = args.subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(args.body, 'html'))

        smtpObj = get_ser_conn(logger, env=env, region_name=region_nm, aplctn_cd="aedl", port=None, tls=True, debug=False)
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()

        logger.info("✅ Email sent successfully.")
        return Message.text(f"✅ Email sent to: {', '.join(recipients)}")
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")
        return Message.text(f"❌ Failed to send email: {e}")
