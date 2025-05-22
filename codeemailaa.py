from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from loguru import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ReduceReuseRecycleGENAI import get_ser_conn

app = FastAPI()

env = "preprod"
region_nm = "us-east-1"
class EmailRequest(BaseModel):
    subject: str
    body: str
    receivers: str

@app.post("/send_test_email")
def send_test_email(email_request: EmailRequest):
    try:
        sender = 'noreply-vkhvkm'
        recipients = [email.strip() for email in receivers.split(",")]

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(body, 'html'))

        smtpObj = get_ser_conn(logger, env=env, region_name=region_nm, aplctn_cd="aedl", port=None, tls=True, debug=False)
        smtpObj.sendmail(sender, recipients, msg.as_string())
        smtpObj.quit()
        logger.info("Email sent successfully.")
        return {"status": " success", "message": " Email sent successfully."}
    except Exception as e:
        logger.error(f" Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f" Error sending email: {e}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
