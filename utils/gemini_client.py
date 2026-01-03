import os
import json
import requests


def call_gemini_api(prompt, api_key=None, system_prompt=None, model_params=None):
    print("Aneesh")
    print(api_key)
    # 🔴 HARD FAIL IF KEY MISSING
    if not api_key:
        return "[System Error] Gemini API key missing."

    model = "gemini-2.0-flash-lite"

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
        f"?key={api_key}"
    )

    full_prompt = f"""
SYSTEM:
{system_prompt}

USER:
{prompt}
"""

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": full_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 512
        }
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
    except Exception as e:
        return f"[Network Error] {e}"

    # 🔴 PRINT RAW RESPONSE ONCE (DEBUG)
    # You can remove this later
    print("📡 Gemini status:", resp.status_code)
    print("📡 Gemini raw:", resp.text[:300])

    if resp.status_code != 200:
        return f"[Gemini Error {resp.status_code}] {resp.text}"

    data = resp.json()

    text = ""
    for c in data.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            text += p.get("text", "")

    # 🔴 ABSOLUTE SAFETY NET
    if not text.strip():
        return (
            "Thank you for reaching out. "
            "We are currently reviewing your issue and will get back to you shortly."
        )

    return text.strip()
