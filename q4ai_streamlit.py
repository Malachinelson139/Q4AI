import streamlit as st
import sqlite3
import google.generativeai as genai

# --------------------
# CONFIGURE GEMINI API
# --------------------
GEMINI_API_KEY = "AIzaSyCwy4G8QdZJ0c8IUdusGgr8InWlf8OcABk"  # Replace with your key
genai.configure(api_key=GEMINI_API_KEY)

# Use latest working Gemini model
MODEL_NAME = "gemini-1.5-flash"

# --------------------
# DATABASE SETUP
# --------------------
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        dob TEXT,
        concerns TEXT
    )
""")
conn.commit()

# --------------------
# STREAMLIT UI
# --------------------
st.set_page_config(page_title="Q4AI Therapist - HealthyMD", page_icon="🧠", layout="centered")

st.title("🧠 Q4AI - HealthyMD Virtual Therapist")
st.write("Welcome to **Q4AI**, your AI-powered mental health assistant, created by **HealthyMD**.")

# Collect patient info
with st.form("patient_form"):
    name = st.text_input("What's your name?")
    age = st.number_input("How old are you?", min_value=0, max_value=120, step=1)
    dob = st.date_input("What's your date of birth?")
    concerns = st.text_area("What's going on? Tell me how you're feeling.")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if not name or not concerns:
        st.error("Please fill in at least your name and concerns.")
    else:
        # Save to database
        cursor.execute("INSERT INTO patients (name, age, dob, concerns) VALUES (?, ?, ?, ?)",
                       (name, age, str(dob), concerns))
        conn.commit()
        st.success(f"Thanks {name}, your information has been securely saved.")

        # AI RESPONSE
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            prompt = f"""
            You are Q4AI, a friendly and empathetic AI therapist working for HealthyMD.
            Speak directly to the patient named {name}, who is {age} years old and was born on {dob}.
            Here is what they are going through: {concerns}.
            Provide emotional support, ask thoughtful follow-up questions, and keep a warm tone.
            """
            response = model.generate_content(prompt)
            st.markdown(f"**Q4AI:** {response.text}")

        except Exception as e:
            st.error(f"⚠️ Error talking to Gemini: {e}")

# --------------------
# VIEW DATABASE (OPTIONAL FOR DEMO)
# --------------------
st.subheader("📋 Stored Patient Records")
if st.checkbox("Show patient database"):
    patients = cursor.execute("SELECT name, age, dob, concerns FROM patients").fetchall()
    for p in patients:
        st.write(f"**Name:** {p[0]}, **Age:** {p[1]}, **DOB:** {p[2]}")
        st.write(f"**Concerns:** {p[3]}")
        st.markdown("---")
