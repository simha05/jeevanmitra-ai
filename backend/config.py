"""
config.py — JeevanMitra AI Backend Configuration
All constants and settings are centralised here.
"""

# ── Server ────────────────────────────────────────────────
PORT      = 8080
HTML_FILE = "frontend/index.html"          # served by the GET handler

# ── Groq REST endpoint ────────────────────────────────────
GROQ_API  = "https://api.groq.com/openai/v1/chat/completions"

# ── Text / chat models (tried in order, skip on 429/503) ─
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "llama3-8b-8192",
]

# ── Vision models (tried in order on failure) ─────────────
VISION_MODELS = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-90b-vision-preview",
]

# ── Cloudflare-friendly headers (fixes HTTP 403 / 1010) ───
HEADERS = {
    "Content-Type":    "application/json",
    "User-Agent":      (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin":          "https://console.groq.com",
    "Referer":         "https://console.groq.com/",
}
