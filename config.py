import os

# Core config
APP_NAME = "HireMate Hiring Assistant"
COMPANY_NAME = "HireMate"
EXIT_KEYWORDS = {"quit","exit","bye","goodbye","stop","end","cancel"}
DEFAULT_MODEL = os.getenv("OPENAI_MODEL","gpt-4o-mini")

# Data paths
DATA_DIR = "data"
CANDIDATES_JSONL = f"{DATA_DIR}/candidates.jsonl"
CANDIDATES_CSV = f"{DATA_DIR}/candidates.csv"

# Privacy
PRIVACY_CONTACT = "privacy@talentscout.example.com"
