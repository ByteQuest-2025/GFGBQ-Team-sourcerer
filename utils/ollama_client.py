import os
import time
import requests
import json
try:
    import openai
except Exception:
    openai = None

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "mistral")


def _call_openai_fallback(prompt, system_prompt=None):
    if not openai:
        return "[Ollama Error] OpenAI SDK not installed for fallback."
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[Ollama Error] Ollama unreachable and OPENAI_API_KEY not set for fallback."
    openai.api_key = api_key
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    try:
        resp = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            max_tokens=512,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI Fallback Error] {e}"


def call_ollama(prompt, system_prompt=None, retries=2, backoff=1.0):
    full_prompt = f"""
SYSTEM:
{system_prompt}

USER:
{prompt}
"""

    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
    }

    last_exc = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "").strip()
        except Exception as e:
            last_exc = e
            # small backoff before retrying
            time.sleep(backoff * (attempt + 1))

    # if we get here, Ollama failed after retries — try OpenAI fallback
    fallback = _call_openai_fallback(prompt, system_prompt)
    if fallback and not fallback.startswith("[Ollama Error]") and not fallback.startswith("[OpenAI Fallback Error]"):
        return fallback
    # return combined error info
    return f"[Ollama Error] {last_exc}; fallback: {fallback}"
