import os
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Database settings
DATABASE_URL = f"sqlite:///{ROOT_DIR}/data/chatbot.db"

# Ensure the data directory exists
os.makedirs(ROOT_DIR / "data", exist_ok=True) 