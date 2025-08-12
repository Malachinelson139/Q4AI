# therapist_sql_bot.py
# This script initializes a SQLite database, collects user information, and interacts with the Gemini AI model
import sqlite3

def init_db():
    conn = sqlite3.connect('therapist_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            dob TEXT,
            concerns TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()
def save_session(name, age, dob, concerns, response):
    conn = sqlite3.connect('therapist_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO sessions (name, age, dob, concerns, response)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, age, dob, concerns, response))
    conn.commit()
    conn.close()


import google.generativeai as genai
# Initialize the database
print("hey how are you doing?")
# ========== CONFIGURE GEMINI ==========
genai.configure(api_key="AIzaSyCwy4G8QdZJ0c8IUdusGgr8InWlf8OcABk")  # Replace this with your key
model = genai.GenerativeModel("models/gemini-2.5-flash")  # Use the appropriate model
print("Model loaded:")
chat = model.start_chat(history=[])

# ========== SETUP DATABASE ==========
conn = sqlite3.connect("clients.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        dob TEXT,
        concerns TEXT
    )
""")
conn.commit()

# ========== COLLECT USER INFO ==========
print("Welcome to Q4AI, your virtual mental health assistant from HealthyMD.\n")

name = input("What is your name? ")
age = input("How old are you? ")
dob = input("What's your date of birth (YYYY-MM-DD)? ")
concerns = input("What’s been going on lately that you’d like to talk about? ")

# Save to DB
cursor.execute("INSERT INTO clients (name, age, dob, concerns) VALUES (?, ?, ?, ?)",
               (name, age, dob, concerns))
conn.commit()

# ========== AI RESPONSE ==========
print("\n🧠 Thinking...\n")

try:
    response = chat.send_message(
        f"My name is {name}, I’m {age} years old. I was born on {dob}. Here's what's going on: {concerns}"
    )
    reply = response.text.strip()
    print("🕊️Q4AI:", reply)
except Exception as e:
    print("⚠️ Error talking to Gemini:", e)

# ========== OPTIONAL: CONTINUED CHAT ==========
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Take care. I'm always here to talk.")
        break

    try:
        response = chat.send_message(user_input)
        print("🤖 AI Therapist:", response.text.strip())
    except Exception as e:
        print("⚠️ Error:", e)

# Close DB connection
conn.close()
