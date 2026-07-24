import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DATABASE_PATH = os.getenv("DATABASE_PATH", "database/secret_beauty.db")