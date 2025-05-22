import requests

# Replace with your EC2 public IP or DNS
EC2_SERVER_URL = "http://3.92.107.123:8000/invoke"  # <-- Update this

# Tool payload
payload = {
    "tool": "mcp-send-email",
    "input": {
        "subject": "🌐 Email from EC2 MCP Server",
        "body": "<p>This email was sent from a FastAPI server running on EC2.</p>",
        "receivers": "you@example.com"
    }
}

try:
    print(f"📡 Sending request to {EC2_SERVER_URL} ...")
    response = requests.post(EC2_SERVER_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    print("✅ Response from server:")
    print(result["content"])
except requests.RequestException as e:
    print("❌ Request failed:")
    print(e)
    if e.response is not None:
        print(e.response.text)
