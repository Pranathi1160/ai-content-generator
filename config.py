"""
Configuration file for AI Content Generator
Loads environment variables and sets default configurations
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1024))

# Application Configuration
APP_TITLE = "AI Blog/Article Generator"
APP_ICON = "📝"

# Content Generation Settings
MIN_LENGTH = 100
MAX_LENGTH = 2000
DEFAULT_LENGTH = 500

# Tone Options
TONE_OPTIONS = ["Professional", "Casual", "Technical"]

# Validation
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in .env file. Please add your API key.")