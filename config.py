import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Application Settings
APP_TITLE = "TalentScout Hiring Assistant"
APP_DESCRIPTION = "AI-powered initial candidate screening for technology positions"
VERSION = "1.0.0"

# Conversation Settings
MAX_CONVERSATION_HISTORY = 50
CONVERSATION_TIMEOUT_MINUTES = 30

# Validation Settings
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_DIGITS = 10
MIN_EXPERIENCE_YEARS = 0
MAX_EXPERIENCE_YEARS = 50

# Technical Question Settings
MIN_TECHNICAL_QUESTIONS = 3
MAX_TECHNICAL_QUESTIONS = 5