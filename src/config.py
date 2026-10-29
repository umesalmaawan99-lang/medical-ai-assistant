import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Key configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configuration
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.2

# Form Options for UI dropdowns/multiselects
GENDER_OPTIONS = ["Female", "Male", "Other", "Prefer not to say"]

SYMPTOM_OPTIONS = [
    "Fever", "Cough", "Headache", "Fatigue", "Sore Throat",
    "Shortness of Breath", "Chest Pain", "Dizziness", "Nausea",
    "Stomach Ache", "Joint Pain", "Runny Nose", "Skin Rash"
]

DURATION_OPTIONS = [
    "Less than 24 hours",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "More than 2 weeks"
]

LANGUAGE_OPTIONS = [
    "English",
    "Urdu",
    "Spanish",
    "French",
    "Arabic",
    "Hindi"
]