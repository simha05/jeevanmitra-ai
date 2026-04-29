# 🌿 JeevanMitra AI — Multilingual Smart Farming Assistant

> An AI-powered agricultural advisor that helps Indian farmers with crop recommendations, yield prediction, disease detection, and real-time market prices — all running **100% locally**, powered by **Groq's free API**.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🌾 **Crop Recommendation** | Soil-sensor-based AI crop suggestions with confidence scores |
| 📊 **Yield Prediction** | ML model for expected harvest per hectare |
| 🔍 **Disease Detection** | Vision AI diagnoses plant diseases from leaf photos |
| 💰 **Market Prices** | Live mandi prices with trend indicators |
| 💬 **Multilingual Chat** | Converse in English, Hindi, Kannada, Malayalam, Tamil, Telugu |
| 🎤 **Voice Input** | Browser-native speech recognition |
| 🔊 **Text-to-Speech** | Reads responses aloud in the selected language |

---

## 🏗️ Project Structure

```
jeevanmitra/
├── backend/
│   ├── __init__.py          # Package marker
│   ├── config.py            # All constants (port, models, headers)
│   ├── groq_client.py       # Groq API wrapper with model fallback
│   ├── handler.py           # HTTP request handler (all routes)
│   └── server.py            # Server startup & browser launch
│
├── frontend/
│   └── index.html           # Single-page app (HTML + CSS + JS)
│
├── run.py                   # ← Entry point: python run.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start (60 seconds)

### 1. Get a Free Groq API Key

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up (free, no credit card)
3. Navigate to **API Keys → Create API Key**
4. Copy the key (starts with `gsk_…`)

### 2. Clone & Run

```bash
# Clone the repo
git clone https://github.com/<your-username>/jeevanmitra.git
cd jeevanmitra

# (Optional) Install vision-model SDK for best image support
pip install -r requirements.txt

# Start the server
python run.py
```

Your browser will open **http://localhost:8080** automatically.

### 3. Enter API Key in the App

Paste your `gsk_…` key when the modal appears → click **Save & Activate**.

---

## 🔧 Configuration

All settings live in **`backend/config.py`**:

| Variable | Default | Description |
|---|---|---|
| `PORT` | `8080` | Local server port |
| `GROQ_API` | Groq endpoint | REST API URL |
| `MODELS` | llama-3.3-70b, … | Text/chat models (fallback order) |
| `VISION_MODELS` | llama-4-scout, … | Vision models (fallback order) |
| `HEADERS` | Cloudflare-safe UA | HTTP headers sent with every request |

---

## 📦 Dependencies

| Package | Purpose | Required? |
|---|---|---|
| Python ≥ 3.10 | Runtime | ✅ Yes |
| `groq` SDK | Vision-model fallback (fixes Cloudflare 403) | Optional |

The core server uses **only Python standard library** — no pip install needed for text chat.

```bash
# Install optional groq SDK for best vision support
pip install groq
# or
pip install -r requirements.txt
```

---

## 🌐 API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend SPA |
| `GET` | `/groq-status` | Returns `{ ok, model, has_key }` |
| `POST` | `/groq-setkey` | Store API key `{ key: "gsk_…" }` |
| `POST` | `/groq` | Proxy chat/vision request to Groq |

### POST `/groq` payload

```json
{
  "prompt": "Which crop suits black soil in Karnataka?",
  "vision": false,
  "image": "<base64-string or null>",
  "mime": "image/jpeg"
}
```

---

## 🌍 Supported Languages

English · हिंदी · ಕನ್ನಡ · മലയാളം · தமிழ் · తెలుగు · বাংলা

---

## 🛡️ Security Notes

- Your Groq API key is stored **only in `localStorage`** in your browser and the **in-memory Python server** — it is never written to disk or logged.
- The server only accepts connections from `localhost` — it is not exposed to the internet.
- **Never commit your API key** to version control (it is covered by `.gitignore`).

---

## 🐛 Troubleshooting

| Issue | Fix |
|---|---|
| HTTP 403 / error 1010 (Cloudflare) | `pip install groq` then restart `python run.py` |
| Invalid key error | Re-enter key; make sure it starts with `gsk_` |
| Rate limit (429) | Wait 30 seconds; free tier resets daily |
| Vision model not found | Your Groq plan may not include vision; try a different model in `config.py` |
| Port 8080 in use | Change `PORT` in `backend/config.py` |

---

## 📄 License

MIT — free to use, modify, and distribute.

---

## 🙏 Built With

- **[Groq](https://groq.com)** — ultra-fast LLM inference (free tier)
- **Python** standard library (`http.server`, `urllib`)
- Vanilla HTML · CSS · JavaScript (no frontend framework)

---

*Made with ❤️ for Indian farmers 🌾*
