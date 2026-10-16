import os

from dotenv import load_dotenv

load_dotenv()

# LLM configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

# Authentication configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)