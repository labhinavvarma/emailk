# router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ReduceReuseRecycleGENAI.smtp_helper import get_ser_conn
from mcpserver import mcp

route = APIRouter()

env = "preprod"
region_nm = "us-east-1"

class EmailRequest(BaseModel):
    subject: str
    body: str
    receivers: str  # comma-separated

@mcp.tool(name="mcp-send-email", description="Send an email using SMTP")
@route.post("/send_test_email", tags=["Email"])
def send_test_email(email_request: EmailRequest):
    try:
        sender = "noreply@example.com"  # Update for valid sender
        recipients = [email.strip() for email in email_request.receivers.split(",")]

        msg = MIMEMultipart()
        msg["Subject"] = email_request.subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(email_request.body, "html"))

        smtpObj = get_ser_conn(
            logger, env=env, region_name=region_nm, aplctn_cd="aedl", port=None, tls=True, debug=False
        )
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()

        logger.info("Email sent successfully.")
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")
