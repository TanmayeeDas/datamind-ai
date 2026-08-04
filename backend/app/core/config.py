from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "DataMind AI")
    DEBUG = os.getenv("DEBUG", "False") == "True"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()
