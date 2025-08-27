import os, json, csv
from typing import Dict, List
from config import CANDIDATES_JSONL, CANDIDATES_CSV, DATA_DIR

os.makedirs(DATA_DIR, exist_ok=True)

CSV_FIELDS = ["full_name","email","phone","years_experience","desired_positions","current_location","tech_stack","answers"]

def save_candidate(profile: Dict):
    # JSONL
    with open(CANDIDATES_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(profile, ensure_ascii=False) + "\n")
    # CSV (create header if missing)
    exists = os.path.exists(CANDIDATES_CSV)
    with open(CANDIDATES_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not exists:
            w.writeheader()
        row = {
            "full_name": profile.get("full_name",""),
            "email": profile.get("email",""),
            "phone": profile.get("phone",""),
            "years_experience": profile.get("years_experience",""),
            "desired_positions": ", ".join(profile.get("desired_positions",[]) or []),
            "current_location": profile.get("current_location",""),
            "tech_stack": ", ".join(profile.get("tech_stack",[]) or []),
            "answers": "; ".join(profile.get("answers",[]) or []),
        }
        w.writerow(row)
