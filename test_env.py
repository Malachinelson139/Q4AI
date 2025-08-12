import os
from dotenv import load_dotenv

load_dotenv()
print("GEMINI_API_KEY =", os.getenv("GEMINI_API_KEY"))
