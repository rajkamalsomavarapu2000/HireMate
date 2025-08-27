import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+]?\d[\d\s().-]{6,}$")

def is_email(text: str) -> bool:
    return bool(text and EMAIL_RE.match(text.strip()))

def is_phone(text: str) -> bool:
    return bool(text and PHONE_RE.match(text.strip()))

def clean_phone(text: str) -> str:
    return re.sub(r"[^\d+]", "", text or "")

def normalize_list(raw):
    if not raw:
        return []
    if isinstance(raw, list):
        return [x.strip() for x in raw if str(x).strip()]
    # split by comma or slash
    return [x.strip() for x in re.split(r"[,/]| and ", str(raw)) if x.strip()]
