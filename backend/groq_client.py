"""
groq_client.py — JeevanMitra AI  |  Groq API wrapper
Handles both text (chat) and vision requests with
automatic model-fallback and SDK fallback for vision.
"""

import json
import urllib.error
import urllib.request

from backend.config import GROQ_API, HEADERS, MODELS, VISION_MODELS

# Runtime-mutable API key (set via /groq-setkey endpoint)
_groq_key: str = ""


# ── Public helpers ─────────────────────────────────────────

def set_key(key: str) -> None:
    """Store the Groq API key received from the frontend."""
    global _groq_key
    _groq_key = key.strip()


def has_key() -> bool:
    return bool(_groq_key)


def get_primary_model() -> str:
    return MODELS[0]


# ── Core chat function ─────────────────────────────────────

def groq_chat(
    prompt: str,
    image_b64: str | None = None,
    image_mime: str = "image/jpeg",
) -> tuple[str, str | None, str]:
    """
    Send a prompt (and optional image) to Groq.

    Returns
    -------
    (text, error, model_used)
      • text       – model reply, empty string on failure
      • error      – human-readable error message or None on success
      • model_used – name of the model that responded
    """
    if not _groq_key:
        return "", "No API key. Enter your Groq key in the app.", ""

    if image_b64:
        messages = [{"role": "user", "content": [
            {"type": "image_url",
             "image_url": {"url": f"data:{image_mime};base64,{image_b64}"}},
            {"type": "text", "text": prompt},
        ]}]
        models_to_try = VISION_MODELS
    else:
        messages = [{"role": "user", "content": prompt}]
        models_to_try = MODELS

    last_err = "Unknown error"

    for model in models_to_try:
        payload = {
            "model":       model,
            "messages":    messages,
            "max_tokens":  1024,
            "temperature": 0.2 if image_b64 else 0.7,
        }
        headers = {**HEADERS, "Authorization": f"Bearer {_groq_key}"}

        try:
            req = urllib.request.Request(
                GROQ_API,
                data=json.dumps(payload).encode(),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read())
            return data["choices"][0]["message"]["content"], None, model

        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace")
            try:
                msg = json.loads(raw).get("error", {}).get("message", raw)
            except Exception:
                msg = raw
            short = msg[:120]
            print(f"  ⚠️  [{model}] HTTP {e.code}: {short}")
            last_err = msg

            if e.code in (429, 503, 403):   # rate-limit / overload / CF block → try next
                continue
            return "", f"HTTP {e.code}: {short}", model   # hard 4xx

        except Exception as ex:
            print(f"  ⚠️  [{model}] {ex}")
            last_err = str(ex)
            continue

    # All urllib attempts failed — try the official Groq SDK as last resort
    if image_b64:
        sdk_result = _try_groq_sdk(prompt, image_b64, image_mime)
        if sdk_result:
            return sdk_result, None, "groq-sdk"

    return "", last_err, ""


# ── SDK fallback (vision only) ─────────────────────────────

def _try_groq_sdk(prompt: str, image_b64: str, image_mime: str) -> str | None:
    """
    Fallback: use the official groq Python SDK which handles
    Cloudflare auth differently.  Requires:  pip install groq
    """
    try:
        from groq import Groq  # type: ignore[import]
        client = Groq(api_key=_groq_key)
        for model in VISION_MODELS:
            try:
                chat = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:{image_mime};base64,{image_b64}"}},
                        {"type": "text", "text": prompt},
                    ]}],
                    max_tokens=1024,
                    temperature=0.2,
                )
                text = chat.choices[0].message.content
                print(f"  ✅ [groq-sdk/{model}] OK")
                return text
            except Exception as ex:
                print(f"  ⚠️  [groq-sdk/{model}] {ex}")
                continue
    except ImportError:
        print("  ℹ️  groq SDK not installed. Run: pip install groq")
    except Exception as ex:
        print(f"  ⚠️  groq SDK error: {ex}")
    return None
