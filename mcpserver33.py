from fastmcp import FastMCP, tool
from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ReduceReuseRecycleGENAI import get_ser_conn
from loguru import logger

# Initialize FastMCP server
mcp = FastMCP(name="EmailMCPServer")

# Define the input schema
class EmailRequest(BaseModel):
    subject: str
    body: str
    receivers: str

# Define the MCP tool
@mcp.tool()
def send_email(subject: str, body: str, receivers: str) -> dict:
    try:
        sender = 'noreply-vkhvkm'
        recipients = [email.strip() for email in receivers.split(",")]

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(body, 'html'))

        smtpObj = get_ser_conn(logger, env="preprod", region_name="us-east-1", aplctn_cd="aedl", port=None, tls=True, debug=False)
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()
        logger.info("Email sent successfully.")
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return {"status": "error", "message": f"Error sending email: {e}"}

# Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
