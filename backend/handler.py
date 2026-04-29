"""
handler.py — JeevanMitra AI  |  HTTP request handler
Handles all routes: static files, API key management,
Groq chat/vision proxy, and CORS preflight.
"""

import http.server
import json
import os

from backend import groq_client
from backend.config import HTML_FILE, MODELS


class JeevanMitraHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP handler for all JeevanMitra routes."""

    # ── Logging ───────────────────────────────────────────────

    def log_message(self, fmt, *args):  # noqa: D401
        pass  # Suppress default access logs for cleaner terminal output

    # ── CORS helpers ──────────────────────────────────────────

    def _add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, status_code: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self._add_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    # ── OPTIONS (CORS preflight) ──────────────────────────────

    def do_OPTIONS(self):
        self.send_response(200)
        self._add_cors_headers()
        self.end_headers()

    # ── GET ───────────────────────────────────────────────────

    def do_GET(self):
        # Status endpoint — polled by the frontend on startup
        if self.path == "/groq-status":
            self._json_response(200, {
                "ok":      groq_client.has_key(),
                "model":   MODELS[0],
                "has_key": groq_client.has_key(),
            })
            return

        # Serve the SPA index
        if self.path in ("/", "/index.html"):
            self.path = f"/{HTML_FILE}"

        filepath = self.path.lstrip("/")
        if os.path.exists(filepath):
            self.send_response(200)
            if filepath.endswith(".html"):
                self.send_header("Content-Type", "text/html; charset=utf-8")
            self._add_cors_headers()
            self.end_headers()
            with open(filepath, "rb") as fh:
                self.wfile.write(fh.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    # ── POST ──────────────────────────────────────────────────

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length))
        except Exception:
            self._json_response(400, {"error": "Invalid JSON"})
            return

        if self.path == "/groq-setkey":
            self._handle_set_key(payload)
        elif self.path == "/groq":
            self._handle_groq(payload)
        else:
            self.send_response(404)
            self.end_headers()

    # ── Route handlers ────────────────────────────────────────

    def _handle_set_key(self, payload: dict):
        groq_client.set_key(payload.get("key", ""))
        status = "set ✅" if groq_client.has_key() else "cleared"
        print(f"  🔑 Groq key {status}")
        self._json_response(200, {"ok": True})

    def _handle_groq(self, payload: dict):
        prompt     = payload.get("prompt", "")
        image_b64  = payload.get("image")
        is_vision  = payload.get("vision", False)
        img_mime   = payload.get("mime", "image/jpeg")

        mode = "vision" if is_vision else "chat"
        print(f"  🤖 Groq {mode} request")

        text, err, model = groq_client.groq_chat(
            prompt,
            image_b64 if is_vision else None,
            img_mime,
        )

        if err:
            friendly = self._friendly_error(err)
            print(f"  ⚠️  {err[:120]}")
            self._json_response(500, {"error": friendly})
            return

        print(f"  ✅ [{model}] OK ({len(text)} chars)")
        self._json_response(200, {"text": text, "_model_used": model})

    # ── Error messaging ───────────────────────────────────────

    @staticmethod
    def _friendly_error(err: str) -> str:
        if "1010" in err or ("403" in err and "cloudflare" in err.lower()):
            return (
                "🚫 Cloudflare blocked the vision request. "
                "Fix: run  pip install groq  then restart the server."
            )
        if "401" in err or "invalid_api_key" in err.lower():
            return "❌ Invalid Groq API key. Please re-enter your key."
        if "429" in err:
            return "⏳ Rate limit reached. Please wait 30 seconds and try again."
        if "model_not_found" in err.lower():
            return "❌ Vision model not available on your Groq plan."
        return err
