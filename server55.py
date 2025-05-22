from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ReduceReuseRecycleGENAI import get_ser_conn
from loguru import logger

# Initialize FastMCP server
mcp = FastMCP(name="EmailMCPServer")

@mcp.tool()
def send_email(subject: str, body: str, receivers: str) -> dict:
    """
    Sends an email to the specified recipients.

    Args:
        subject (str): Subject of the email.
        body (str): HTML content of the email.
        receivers (str): Comma-separated list of recipient email addresses.

    Returns:
        dict: Status message indicating success or failure.
    """
    try:
        sender = 'noreply-vkhvkm'
        recipients = [email.strip() for email in receivers.split(",")]

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(body, 'html'))

        # Establish SMTP connection using your custom function
        smtpObj = get_ser_conn(
            logger,
            env="preprod",
            region_name="us-east-1",
            aplctn_cd="aedl",
            port=None,
            tls=True,
            debug=False
        )
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()
        logger.info("Email sent successfully.")
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return {"status": "error", "message": f"Error sending email: {e}"}

@mcp.prompt()
def compose_email_prompt(subject: str, body: str, receivers: str) -> str:
    """
    Generates a prompt instructing the LLM to send an email with the provided details.

    Args:
        subject (str): Subject of the email.
        body (str): Body content of the email.
        receivers (str): Comma-separated list of recipient email addresses.

    Returns:
        str: A prompt message for the LLM.
    """
    return (
        f"Please send an email with the following details:\n"
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"Recipients: {receivers}"
    )

if __name__ == "__main__":
    # Run the MCP server using Streamable HTTP transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
