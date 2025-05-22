import requests

# Replace with your actual server URL or IP
MCP_SERVER_URL = "http://localhost:8000/invoke"

# Define the input payload for the tool
payload = {
    "tool": "mcp-send-email",
    "input": {
        "subject": "🚀 MCP Client Test Email",
        "body": "<h3>Hello from the client</h3><p>This email was sent using the MCP server.</p>",
        "receivers": "youremail@example.com,another@example.com"
    }
}

try:
    response = requests.post(MCP_SERVER_URL, json=payload)
    response.raise_for_status()
    print("✅ Tool Response:")
    print(response.json()["content"])
except requests.RequestException as e:
    print("❌ Request failed:")
    print(e)
    if e.response is not None:
        print(e.response.text)
