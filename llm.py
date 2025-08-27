import os, json
from typing import List, Dict, Optional
from openai import OpenAI
from config import DEFAULT_MODEL

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def chat(messages: List[Dict], model: str = None, temperature: float = 0.2) -> Dict:
    client = _get_client()
    res = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        temperature=temperature,
        messages=messages
    )
    return res.choices[0].message

def complete_json(system_prompt: str, user_prompt: str, temperature: float = 0.1) -> Optional[Dict]:
    """Return parsed JSON dict or None on failure."""
    try:
        msg = chat(
            [
                { "role": "system", "content": system_prompt.strip() },
                { "role": "user", "content": user_prompt.strip() },
            ],
            temperature=temperature
        )
        content = (msg.content or "").strip()
        # Extract possible JSON
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            js = content[start:end+1]
            return json.loads(js)
        return None
    except Exception:
        return None
