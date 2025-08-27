from typing import List, Dict
from config import COMPANY_NAME, EXIT_KEYWORDS
from privacy import PRIVACY_NOTICE

# ---------- STAR Prompt Builders ----------

def star_greeting_prompt(missing_fields: List[str]) -> str:
    fields_str = ", ".join(missing_fields) if missing_fields else "none"
    return f"""
# STAR Prompt — Greeting & Onboarding

Situation:
You are an AI Hiring Assistant for {COMPANY_NAME}. A candidate has just started a chat.

Task:
Greet the candidate warmly, state your purpose (initial screening), show brief privacy notice, and request only the first 2 missing fields to keep the flow light. Keep scope to hiring only.

Action:
- One-paragraph friendly greeting + single-sentence privacy reminder.
- Ask specifically for the next 2 missing fields from: {fields_str}.
- Offer that they can type one of these keywords to end at any time: {', '.join(sorted(EXIT_KEYWORDS))}.

Result:
A concise, friendly message that keeps momentum while respecting privacy.
"""

def star_extract_prompt(user_input: str, fields_needed: List[str]) -> str:
    needed = ", ".join(fields_needed) if fields_needed else "none"
    return f"""
# STAR Prompt — Information Extraction

Situation:
A candidate wrote: \"\"\"{user_input}\"\"\".

Task:
Extract any of these fields if present (even implicitly): {needed}.
Fields set: full_name, email, phone, years_experience, desired_positions (list), current_location, tech_stack (list).

Action:
- Output STRICT JSON ONLY with keys among the above. 
- Do not add commentary. Do not include example values. Missing keys must be omitted.
- For lists (desired_positions, tech_stack), output an array of strings.
- Normalize years_experience to a number if possible.

Result:
A minimal JSON object with the extracted fields only.
"""

def star_missing_fields_prompt(profile: Dict) -> str:
    missing = [k for k in ["full_name","email","phone","years_experience","desired_positions","current_location","tech_stack"] if not profile.get(k)]
    fields_str = ", ".join(missing) if missing else "none"
    return f"""
# STAR Prompt — Ask for Missing Fields

Situation:
We are collecting candidate profile fields. The following are still missing: {fields_str}.

Task:
Ask for the next 2–3 missing items in a natural conversational way, one message, concise.

Action:
- Keep to hiring scope. One friendly paragraph.
- Use bullet points if you ask for more than one item.
- Remind that they can end anytime with keywords and we will save their progress.

Result:
A short, clear question that helps complete the profile.
"""

def star_question_gen_prompt(tech_stack: List[str], desired_positions: List[str]) -> str:
    stack_str = ", ".join(tech_stack) if tech_stack else "none"
    roles = ", ".join(desired_positions) if desired_positions else "general SWE"
    return f"""
# STAR Prompt — Technical Question Generation

Situation:
A candidate declared their tech stack: [{stack_str}] and is applying for roles: {roles}.

Task:
Generate 3–5 concise, probing technical questions for EACH technology named to test practical proficiency.

Action:
- Prefer scenario-based or depth-probing questions over trivia.
- Increase difficulty slightly if the stack suggests seniority.
- No answers, no hints, no code blocks unless essential.
- Return STRICT JSON ONLY of the form:
  {{
    "questions": [ {{"tech": "<name>", "items": ["Q1", "Q2", "Q3"]}}, ... ]
  }}
- Cap total questions at 12 across all technologies if there are many.

Result:
A compact JSON object containing targeted questions per technology.
"""

def star_fallback_prompt(user_input: str) -> str:
    return f"""
# STAR Prompt — Fallback / Repair

Situation:
The latest user message was unclear for a hiring context:
\"\"\"{user_input}\"\"\"

Task:
Gently steer back on track with a clarifying question or a brief explanation of acceptable inputs.

Action:
- One or two sentences max.
- Offer examples (like "Python, Django" or "3 years, Backend Engineer").

Result:
A polite nudge that helps the candidate continue productively.
"""

def star_wrapup_prompt(profile: Dict) -> str:
    name = profile.get("full_name","there")
    return f"""
# STAR Prompt — Wrap-up

Situation:
We have collected the key details and asked technical questions.

Task:
Thank {name}, explain next steps, and close politely.

Action:
- One paragraph max.
- Mention that our team will review and contact them if there's a fit.
- Remind them they can type 'delete my data' to remove local session data (demo).

Result:
A graceful closing message.
"""
