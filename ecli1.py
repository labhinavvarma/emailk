import requests
import json

# Server URL (change if hosted elsewhere)
SERVER_URL = "http://localhost:8000/send_test_email"

# Sample email payload
email_payload = {
    "subject": "Test MCP Email",
    "body": "<h3>This is a test email sent from MCP client.</h3>",
    "receivers": "example1@domain.com,example2@domain.com"
}

# Send POST request
response = requests.post(SERVER_URL, json=email_payload)

# Output result
if response.status_code == 200:
    print("✅ Email sent successfully.")
    print(response.json())
else:
    print(f"❌ Failed to send email: {response.status_code}")
    print(response.text)
