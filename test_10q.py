import requests

# 1. SETTINGS
# Go to your n8n Webhook node -> Click "Test URL" tab -> Copy it.
# It should look like: https://.../webhook-test/10q-chat
url = "https://robertnowak30.app.n8n.cloud/webhook-test/10q-chat"

# 2. THE QUESTION
# Ask something specific to your 10Q documents
question = "What are the primary risk factors mentioned in Apple's 10Q?"

# 3. SEND IT
print(f"🤖 Asking Agent: '{question}'...")
try:
    response = requests.post(url, json={"query": question})
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Answer:")
        print(response.text) # or response.json() if you formatted it
    else:
        print(f"\n❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")