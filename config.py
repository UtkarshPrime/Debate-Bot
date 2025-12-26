import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
MAX_ROUNDS = 8
LOG_DIR = "logs"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() == "true"

# Persona Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONA_DIR = os.path.join(BASE_DIR, "personas")
SCIENTIST_PERSONA_PATH = os.path.join(PERSONA_DIR, "scientist.txt")
PHILOSOPHER_PERSONA_PATH = os.path.join(PERSONA_DIR, "philosopher.txt")

# Ensure log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
