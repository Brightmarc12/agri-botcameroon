# 🌾 Agri-Bot Cameroon API

**Agri-Bot Cameroon** is a multilingual AI agent that provides key agricultural information for farmers in Cameroon. It supports Telex.im’s A2A protocol and a simple REST API.

🔗 **Live API Endpoints:**
- AWS Elastic Beanstalk (primary): `http://Agri-bot-cameroon-env.eba-hmxpx9yd.us-east-1.elasticbeanstalk.com/agent`
- Render (backup): `https://agri-botcameroon.onrender.com/agent`

---

## ✨ Features

*   💰 **Market Prices:** Cocoa, coffee, maize, etc.
*   🦠 **Pest & Disease Diagnosis**
*   🌤️ **Localized Weather Forecasts**
*   🌱 **Best Farming Practices**
*   🌍 **Soil Information**
*   💊 **Fertilizer Guide**
*   🌍 **Multilingual:** English and French

---

## 📡 API Usage (Simple REST)

Send a **POST** with a JSON body.

**Endpoint:** `http://Agri-bot-cameroon-env.eba-hmxpx9yd.us-east-1.elasticbeanstalk.com/agent`  
**Method:** `POST`  
**Headers:** `Content-Type: application/json`

### 📝 Request Body
```json
{
  "message": "what is the price of cocoa"
}
```

### 📚 Example (REST)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "what is the price of cocoa"}' \
  http://Agri-bot-cameroon-env.eba-hmxpx9yd.us-east-1.elasticbeanstalk.com/agent
```

Expected response:
```json
{
  "response": "The current market price for cocoa is 1,500 XAF per kg."
}
```

---

## 🤝 Telex.im A2A Integration
This agent natively handles Telex A2A JSON‑RPC requests.

### A2A Request Example (what Telex sends)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "id": "123",
    "params": {
      "message": {
        "parts": [ { "kind": "text", "text": "quel est le prix du cacao" } ]
      }
    }
  }' \
  http://Agri-bot-cameroon-env.eba-hmxpx9yd.us-east-1.elasticbeanstalk.com/agent
```
A2A response (JSON‑RPC):
```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "result": {
    "message": {
      "parts": [ { "text": "Le prix actuel du marché pour cacao est de 1,500 XAF per kg.", "contentType": "text/plain" } ]
    }
  }
}
```

### Import into Telex
1. Open your coworker → Task List → “Paste Workflow JSON”.  
2. Paste the contents of `agri_bot_workflow.json` and Save.  
3. Click **Publish** on the coworker.  
4. Add the coworker to your channel and test.

Agent logs (replace with your channel id):  
`https://api.telex.im/agent-logs/{channel-id}.txt`

---

## 🚀 Run Locally

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
flask run
```
App runs at `http://127.0.0.1:5000`.

---

## 🛠️ Tech Stack

* 🐍 **Language:** Python
* 🌶️ **Framework:** Flask
* ⚙️ **Server:** Gunicorn
* ☁️ **Deployment:** AWS Elastic Beanstalk (Primary) | Render (Backup)
* 🤝 **Integration:** Telex.im A2A Protocol