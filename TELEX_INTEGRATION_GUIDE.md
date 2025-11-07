# 🔌 Agri-Bot Cameroon - Telex.im Integration Guide

## 📋 Overview

This guide explains how to integrate Agri-Bot Cameroon with Telex.im using the A2A (Agent-to-Agent) protocol. The agent is built with Python/Flask and is fully compatible with the Telex platform.

---

## ✅ What Was Fixed

### Problem
The original implementation only supported simple JSON format (`{"message": "text"}`), but Telex.im with A2A protocol sends JSON-RPC 2.0 requests with a more complex structure.

### Solution
Updated the `/agent` endpoint to support **both formats**:
1. **A2A JSON-RPC 2.0 format** (from Telex/Mastra)
2. **Simple REST format** (for testing)

---

## 🔧 Technical Implementation

### Dual Format Support

The agent now automatically detects the request format and responds appropriately:

```python
@app.route('/agent', methods=['POST'])
def telex_agent():
    incoming_data = request.get_json()
    
    # Handle A2A JSON-RPC format
    if incoming_data.get('jsonrpc') == '2.0':
        # Extract message from A2A structure
        # Return A2A-compliant response
        return jsonify({
            "jsonrpc": "2.0",
            "id": incoming_data.get('id'),
            "result": {
                "role": "assistant",
                "parts": [{"kind": "text", "text": response_text}]
            }
        })
    
    # Handle simple JSON format (for testing)
    # Return {"response": "text"}
```

### Request Format Examples

#### A2A JSON-RPC Format (Telex sends this):
```json
{
  "jsonrpc": "2.0",
  "method": "message",
  "id": 123,
  "params": {
    "message": {
      "parts": [
        {
          "text": "what is the price of cocoa?",
          "contentType": "text/plain"
        }
      ]
    }
  }
}
```

#### Simple JSON Format (for testing):
```json
{
  "message": "what is the price of cocoa?"
}
```

### Response Formats

#### A2A Response:
```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "role": "assistant",
    "parts": [
      {
        "kind": "text",
        "text": "The current market price for cocoa is 1,500 XAF per kg."
      }
    ]
  }
}
```

#### Simple Response:
```json
{
  "response": "The current market price for cocoa is 1,500 XAF per kg."
}
```

---

## 🚀 Integration Steps

### Step 1: Deploy Your Agent

Your agent is already deployed on AWS Elastic Beanstalk:
```
http://Agri-bot-cameroon-env.eba-hmxpx9yd.us-east-1.elasticbeanstalk.com/agent
```

### Step 2: Import Workflow JSON

1. Open Telex.im in your browser
2. Navigate to your workspace
3. Go to "AI Coworkers" → "Add New"
4. Import the `agri_bot_workflow.json` file

### Step 3: Configure the Agent

The workflow is pre-configured with your deployment endpoint. No changes needed!

### Step 4: Test the Integration

1. Create a channel in your Telex workspace
2. Add the "agri_bot_cameroon" agent to the channel
3. Send a test message: `@agri_bot_cameroon what is the price of cocoa?`
4. The agent should respond with current prices

---

## 🐛 Debugging

### Check Agent Logs

View agent interaction logs at:
```
https://api.telex.im/agent-logs/{channel-id}.txt
```

Replace `{channel-id}` with your Telex channel ID (first UUID from channel URL).

### Server-Side Debugging

The agent now includes comprehensive debug logging:

```python
print(f"DEBUG: Received request: {incoming_data}")
print(f"DEBUG: Request headers: {dict(request.headers)}")
```

Check your AWS CloudWatch logs or Elastic Beanstalk logs to see incoming requests.

### Common Issues

#### Issue 1: Agent Not Responding
- **Check**: Is the endpoint publicly accessible?
- **Check**: Are CORS headers configured?
- **Fix**: Ensure your deployment is running and healthy

#### Issue 2: Wrong Response Format
- **Check**: Are logs showing A2A format or simple JSON?
- **Fix**: The agent now handles both automatically

#### Issue 3: Empty Messages
- **Check**: Are messages being extracted correctly?
- **Fix**: Logs will show the incoming structure

---

## 📁 File Structure

```
agri-botcameroon/
├── app.py                      # Main Flask application with dual format support
├── agri_bot_workflow.json     # Telex workflow configuration
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
├── README.md                   # Project documentation
└── TELEX_INTEGRATION_GUIDE.md # This file
```

---

## 🎯 Key Features

### ✅ Dual Format Support
Automatically detects and responds in the correct format

### ✅ Debug Logging
Comprehensive logging for troubleshooting

### ✅ Error Handling
Graceful fallback if request format is unexpected

### ✅ Multilingual
Responds in English and French based on user input

### ✅ Production Ready
Deployed on AWS with proper error handling

---

## 🔗 Resources

- **Telex.im Docs**: https://docs.telex.im/
- **A2A Protocol**: https://docs.telex.im/docs/Agents/overview
- **GitHub Repo**: https://github.com/Brightmarc12/agri-botcameroon
- **Live Endpoint**: http://Agri-bot-cameroon-env.eba-hmxpx9yd.us-east-1.elasticbeanstalk.com/agent

---

## 📞 Support

If you encounter any issues:

1. Check the logs at `https://api.telex.im/agent-logs/{channel-id}.txt`
2. Check AWS CloudWatch for server errors
3. Verify the endpoint is accessible
4. Review the request/response format in logs

---

## 🎉 Success Checklist

- [x] Agent deployed on AWS
- [x] Dual format support implemented
- [x] Debug logging added
- [x] Workflow JSON configured
- [x] Documentation complete
- [x] Error handling implemented
- [x] Multilingual support working
- [ ] Integration tested on Telex
- [ ] Blog post written
- [ ] Tweet shared

---

**Good luck with your integration!** 🚀🌾

