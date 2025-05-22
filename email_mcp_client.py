import requests

# MCP server URL
MCP_SERVER_URL = "http://localhost:8000/invoke"

# Define the tool name and input payload
payload = {
    "tool": "mcp-send-email",
    "input": {
        "subject": "🚀 MCP Email Test",
        "body": "<h2>Hello from MCP Client!</h2><p>This is a test email sent via MCP server.</p>",
        "receivers": "recipient1@example.com, recipient2@example.com"  # Replace with real emails
    }
}

# Send POST request to MCP server
response = requests.post(MCP_SERVER_URL, json=payload)

# Print response
if response.status_code == 200:
    result = response.json()
    print("✅ Email Tool Response:")
    print(result.get("content", result))
else:
    print("❌ Failed to invoke tool")
    print(f"Status: {response.status_code}")
    print(response.text)
