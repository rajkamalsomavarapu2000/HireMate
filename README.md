# 🧭 HireMate — Hiring Assistant Chatbot

An intelligent AI-powered Hiring Assistant built with Streamlit and OpenAI LLMs for TalentScout, a fictional recruitment agency.

The chatbot screens candidates by collecting profile details and asking tech-stack–specific questions. All prompts are designed in STAR format (Situation, Task, Action, Result) for clarity and structure.

# 🚀 Features

🤝 Greeting & Onboarding: Welcomes candidates, shares privacy notice, and starts the screening.

📋 Profile Information Gathering: Collects:

Full Name

Email Address

Phone Number

Years of Experience

Desired Position(s)

Current Location

Tech Stack

⚙️ Tech-Stack Based Questions: Generates 3–5 questions per technology using LLMs (with fallback bank).

🧠 Context-Aware Flow: Maintains conversation context and asks only missing details.

🔄 Fallback & Error Handling: Polite nudges when input is unclear, without breaking flow.

🔚 Conversation End: Wraps up gracefully with next steps or exits when user types keywords (e.g., exit, bye).

🔒 Privacy-First: Data stored locally (JSONL & CSV) for demo purposes; .env and data files are excluded from GitHub.

# Quickstart

Clone the repo:

git clone https://github.com/<your-username>/talentscout-bot.git
cd talentscout-bot


Install dependencies:

pip install -r requirements.txt


Add your OpenAI key:

cp .env.example .env
#edit .env → fill OPENAI_API_KEY=sk-...


Run the app:

streamlit run app.py


Open the browser (default: http://localhost:8501) and chat with the bot.

End anytime with: exit, bye, quit, stop, cancel.

Type "delete my data" to clear session data (demo only).

# 🧠 STAR Prompting

All core prompts are engineered in STAR format:

star_greeting_prompt() → greet, share privacy, ask for 1–2 missing fields.

star_extract_prompt() → JSON-only extractor of profile details from free text.

star_missing_fields_prompt() → politely ask for missing fields.

star_question_gen_prompt() → generate JSON of per-tech questions.

star_fallback_prompt() → redirect back when input is unclear.

star_wrapup_prompt() → close politely with next steps.

# 📊 Example Interaction

Candidate input:

Hi, I’m Raj. I’ve got 2 years of experience in backend roles.  
I work with Python, Django, and SQL. Based in Hyderabad.  
My email is raj@example.com, phone +91 9876543210.


Bot flow:

Extracts name, experience, email, phone, location, desired role, tech stack.

Confirms details and generates questions:

Python → list vs tuple, generators, GIL.

Django → MVT, migrations, QuerySets.

SQL → normalization, joins, indexing.

Asks each Q sequentially, saves answers.

Wraps up politely with next steps.

# 🔒 Data Privacy

Candidate data is stored locally in data/ (JSONL + CSV).

API keys are loaded from .env (never pushed to GitHub).

For production, integrate secure DB + encrypted storage.

# 🌐 Deployment

Works out of the box on Streamlit Community Cloud or platforms like Render, Railway, AWS EC2.

Add your OPENAI_API_KEY in platform’s Environment Variables/Secrets section.
