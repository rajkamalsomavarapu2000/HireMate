import os, json, time
import streamlit as st
from dotenv import load_dotenv

from config import APP_NAME, COMPANY_NAME, EXIT_KEYWORDS
from privacy import PRIVACY_NOTICE
from conversation import greet, handle_user_message
from storage import save_candidate

load_dotenv()

st.set_page_config(page_title=APP_NAME, page_icon="🪐", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.title("🙌 HireMate")
    st.caption("Intelligent Hiring Assistant (demo)")
    st.markdown(PRIVACY_NOTICE)
    st.divider()
    st.markdown("**End anytime:** " + ", ".join(sorted(EXIT_KEYWORDS)))
    st.caption("Model: " + os.getenv("OPENAI_MODEL","gpt-4o-mini"))

# --- Session state ---
if "profile" not in st.session_state:
    st.session_state.profile = {
        "full_name": "",
        "email": "",
        "phone": "",
        "years_experience": "",
        "desired_positions": [],
        "current_location": "",
        "tech_stack": []
    }
if "qa" not in st.session_state:
    st.session_state.qa = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "init_done" not in st.session_state:
    st.session_state.init_done = False
if "finished" not in st.session_state:
    st.session_state.finished = False

st.title(f"🧭 {COMPANY_NAME} Hiring Assistant")

# --- Initial greeting ---
if not st.session_state.init_done:
    msg = greet(st.session_state.profile)
    st.session_state.history.append({"role":"assistant","content":msg})
    st.session_state.init_done = True

# --- Chat display ---
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- User input ---
user_text = st.chat_input("Type here (e.g., 'I'm Raj, 2 yrs exp, Python/Django, Backend Engineer')")
if user_text and not st.session_state.finished:
    st.session_state.history.append({"role":"user","content":user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    reply, profile, qa_state, done = handle_user_message(user_text, st.session_state.profile, st.session_state.qa)
    st.session_state.profile = profile
    st.session_state.qa = qa_state

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.history.append({"role":"assistant","content":reply})

    if done:
        st.session_state.finished = True
        # Auto-save profile locally (demo only)
        try:
            save_candidate(st.session_state.profile)
        except Exception as e:
            st.sidebar.error(f"Failed to save locally: {e}")

# --- Footer controls ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Reset chat"):
        st.session_state.clear()
        st.rerun()
with col2:
    if st.button("🗑 Delete my data (session)"):
        # Just clear session for this demo
        st.session_state.clear()
        st.rerun()
with col3:
    st.caption("© TalentScout (demo)")
