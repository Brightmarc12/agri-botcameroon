# 🌾 Agri-Bot Cameroon API

**Agri-Bot Cameroon** is a versatile, multilingual AI agent designed to provide critical agricultural information to farmers in Cameroon. It operates via a simple JSON API endpoint, making it easy to integrate with platforms like Telex.im. The agent provides real-time market prices, pest/disease diagnosis, weather forecasts, farming best practices, and more, in both English and French.

🔗 **Live API Endpoint:** `https://agri-botcameroon.onrender.com/agent`

---

## ✨ Features

*   💰 **Market Prices:** Get current prices for major crops (cocoa, coffee, maize, etc.).
*   🦠 **Pest & Disease Diagnosis:** Offers preliminary diagnosis and recommendations for common crop problems.
*   🌤️ **Localized Weather Forecasts:** Provides simple weather updates for major Cameroonian cities.
*   🌱 **Best Farming Practices:** Delivers actionable tips on topics like storage, irrigation, and crop-specific care.
*   🌍 **Soil Information:** Gives insights into soil types and suitable crops for different regions.
*   💊 **Fertilizer Guide:** Suggests appropriate fertilizers for key crops.
*   🌍 **Multilingual Support:** All features are accessible in both English and French.

---

## 📡 API Usage

To interact with the agent, send a **POST** request to the live endpoint with a JSON body.

**Endpoint:** `https://agri-botcameroon.onrender.com/agent`  
**Method:** `POST`  
**Headers:** `Content-Type: application/json`

### 📝 Request Body Format

The request body must contain a JSON object with a `message` key.

```json
{
  "sender": "user_id_123",
  "message": "Your query for the agent"
}
```

### 📚 Example API Calls

Here are some examples using curl. You can use any API client like Postman as well.

#### 1️⃣ Getting a Price (English)

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"message": "what is the price of cocoa?"}' \
https://agri-botcameroon.onrender.com/agent
```

**Expected Response:**
```json
{
  "response": "The current market price for cocoa is 1,500 XAF per kg."
}
```

#### 2️⃣ Getting a Price (French)

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"message": "quel est le prix du cacao"}' \
https://agri-botcameroon.onrender.com/agent
```

**Expected Response:**
```json
{
  "response": "Le prix actuel du marché pour cacao est de 1,500 XAF per kg."
}
```

#### 3️⃣ Diagnosing a Problem

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"message": "I have a problem with my maize it has yellow leaves"}' \
https://agri-botcameroon.onrender.com/agent
```

**Expected Response:**
```json
{
  "response": "Indicates a nitrogen deficiency. Recommendation: Apply a nitrogen-rich fertilizer like Urea."
}
```

---

## 🚀 Running the Project Locally

To run this project on your own machine:

### 1️⃣ Clone the repository:
```bash
git clone https://github.com/Brightmarc12/agri-botcameroon.git
cd agri-bot-cameroon
```

### 2️⃣ Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```

### 3️⃣ Install the dependencies:
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask application:
```bash
flask run
```

The application will be running at http://127.0.0.1:5000.

---

## 🛠️ Tech Stack

* 🐍 **Language:** Python
* 🌶️ **Framework:** Flask
* ⚙️ **Server:** Gunicorn
* ☁️ **Deployment:** Render