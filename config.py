from dotenv import load_dotenv
import os

from pathlib import Path

env_path = Path(__file__).parent / "project.env"

load_dotenv(env_path)
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
