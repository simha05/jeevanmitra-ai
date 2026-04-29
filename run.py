#!/usr/bin/env python3
"""
run.py — JeevanMitra AI
━━━━━━━━━━━━━━━━━━━━━━━
Quick-start entry point.  Just run:

    python run.py

Then open http://localhost:8080 in your browser.
"""

import sys
import os

# Ensure project root is on the path so `backend` is importable
sys.path.insert(0, os.path.dirname(__file__))

from backend.server import main

if __name__ == "__main__":
    main()
