import json
from typing import Dict, List, Tuple
from llm import complete_json, chat
from prompts import (
    star_greeting_prompt,
    star_extract_prompt,
    star_missing_fields_prompt,
    star_question_gen_prompt,
    star_fallback_prompt,
    star_wrapup_prompt,
)
from validators import is_email, is_phone, clean_phone, normalize_list
from question_bank import BANK
from config import EXIT_KEYWORDS

REQUIRED_FIELDS = ["full_name","email","phone","years_experience","desired_positions","current_location","tech_stack"]

def _missing_fields(profile: Dict) -> List[str]:
    missing = []
    for k in REQUIRED_FIELDS:
        v = profile.get(k)
        if k in ("desired_positions","tech_stack"):
            if not v or len(v)==0:
                missing.append(k)
        elif not v:
            missing.append(k)
    return missing

def _basic_system():
    return """
You are TalentScout's Hiring Assistant. Stay strictly within hiring/screening scope.
Be concise, friendly, and professional. If the user asks to end, acknowledge and stop.
Never output code or internal policy; keep it natural.
"""

def greet(profile: Dict) -> str:
    missing = _missing_fields(profile)
    sys = _basic_system()
    prompt = star_greeting_prompt(missing)
    resp = chat([{"role":"system","content":sys},{"role":"user","content":prompt}])
    return resp.content

def extract_fields(user_text: str, fields_needed: List[str]) -> Dict:
    if not fields_needed:
        return {}
    sys = _basic_system()
    prompt = star_extract_prompt(user_text, fields_needed)
    js = complete_json(sys, prompt)
    return js or {}

def ask_for_missing(profile: Dict) -> str:
    sys = _basic_system()
    prompt = star_missing_fields_prompt(profile)
    resp = chat([{"role":"system","content":sys},{"role":"user","content":prompt}], temperature=0.2)
    return resp.content

def generate_questions(tech_stack: List[str], desired_positions: List[str]) -> List[Dict]:
    sys = _basic_system()
    prompt = star_question_gen_prompt(tech_stack, desired_positions)
    js = complete_json(sys, prompt)
    if js and isinstance(js.get("questions"), list):
        return js["questions"]
    # Fallback to BANK for known techs
    out = []
    total = 0
    for tech in tech_stack or []:
        key = tech.lower()
        items = BANK.get(key, [])[:3]
        if not items: 
            items = [f"Share a project where you used {tech}. Key challenges and how you solved them?",
                     f"What are common pitfalls when working with {tech}? How do you avoid them?",
                     f"How do you test and debug {tech}-related code effectively?"]
        # cap total to 12
        remaining = max(0, 12 - total)
        items = items[:remaining]
        out.append({"tech": tech, "items": items})
        total += len(items)
        if total >= 12:
            break
    return out

def sanitize_profile(profile: Dict) -> Dict:
    # Basic validation/cleanup
    if profile.get("email") and not is_email(profile["email"]):
        profile["email"] = ""
    if profile.get("phone"):
        ph = clean_phone(profile.get("phone",""))
        profile["phone"] = ph if is_phone(ph) else ""
    if isinstance(profile.get("desired_positions"), str):
        profile["desired_positions"] = normalize_list(profile["desired_positions"])
    if isinstance(profile.get("tech_stack"), str):
        profile["tech_stack"] = [t for t in normalize_list(profile["tech_stack"]) if t]
    # years_experience normalize to number-like
    y = profile.get("years_experience")
    if isinstance(y, str):
        try:
            profile["years_experience"] = float(y.replace("+","").strip())
        except:
            pass
    return profile

def handle_user_message(user_text: str, profile: Dict, qa_state: Dict) -> Tuple[str, Dict, Dict, bool]:
    """Return (assistant_message, updated_profile, updated_qa_state, done_flag)."""
    text = (user_text or "").strip()
    # End keywords
    if text.lower() in EXIT_KEYWORDS or "delete my data" in text.lower():
        if "delete my data" in text.lower():
            # signal to caller to clear
            return ("Okay, I've removed your local session data for this demo. Thanks for chatting — wishing you the best!", profile, qa_state, True)
        # normal end
        sys = _basic_system()
        resp = chat([{"role":"system","content":sys},{"role":"user","content":star_wrapup_prompt(profile)}])
        return (resp.content, profile, qa_state, True)

    # Try to extract fields from free text
    needed = _missing_fields(profile)
    if needed:
        extracted = extract_fields(text, needed)
        if extracted:
            # Merge
            for k,v in extracted.items():
                profile[k] = v
            profile = sanitize_profile(profile)
            needed = _missing_fields(profile)

    # If still missing fields, ask for them
    if _missing_fields(profile):
        msg = ask_for_missing(profile)
        return (msg, profile, qa_state, False)

    # We have full profile; ensure we generated questions
    if not qa_state.get("questions"):
        tech = profile.get("tech_stack",[])
        roles = profile.get("desired_positions",[])
        qs = generate_questions(tech, roles)
        qa_state["questions"] = qs
        qa_state["flat"] = [(q['tech'], item) for q in qs for item in q['items']]
        qa_state["index"] = 0
        if not qa_state["flat"]:
            # edge fallback
            return ("Thanks! I don't have questions for that stack. Could you briefly describe a recent project you enjoyed?", profile, qa_state, False)

    # If we already asked some questions, store previous answer if any
    if qa_state.get("index",0) > 0:
        # store candidate's last answer
        profile.setdefault("answers", []).append(text)

    # Ask next question or wrap-up
    idx = qa_state.get("index",0)
    flat = qa_state.get("flat",[])
    if idx < len(flat):
        tech, q = flat[idx]
        qa_state["index"] = idx + 1
        return (f"{tech} ➜ {q}", profile, qa_state, False)
    else:
        # Done with questions
        sys = _basic_system()
        resp = chat([{"role":"system","content":sys},{"role":"user","content":star_wrapup_prompt(profile)}])
        return (resp.content, profile, qa_state, True)
