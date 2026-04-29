"""
server.py — JeevanMitra AI  |  Main server entry point
Starts the HTTP server and opens the browser automatically.
"""

import http.server
import os
import sys
import threading
import webbrowser

from backend.config import HTML_FILE, PORT
from backend.handler import JeevanMitraHandler


def _open_browser():
    """Delayed browser open so the server is ready first."""
    import time
    time.sleep(1.2)
    webbrowser.open(f"http://localhost:{PORT}")


def main():
    # Ensure the frontend file exists before starting
    if not os.path.exists(HTML_FILE):
        print(f"❌  '{HTML_FILE}' not found.")
        print("   Make sure the frontend/index.html file is present.")
        input("Press Enter to exit...")
        sys.exit(1)

    print("=" * 60)
    print("  🌿  JeevanMitra AI — Groq-Powered Smart Farming Assistant")
    print("=" * 60)
    print(f"  🌐  Open:       http://localhost:{PORT}")
    print(f"  🔑  Get key:    https://console.groq.com  (free, 60 sec)")
    print(f"  📦  Vision fix: pip install groq")
    print(f"  🛑  Stop:       Ctrl+C")
    print("=" * 60)

    threading.Thread(target=_open_browser, daemon=True).start()

    server = http.server.HTTPServer(("localhost", PORT), JeevanMitraHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑  Server stopped.")


if __name__ == "__main__":
    main()
