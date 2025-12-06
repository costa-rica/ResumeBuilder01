import os
from dotenv import load_dotenv

load_dotenv()

URL_BASE_OPENAI = os.getenv("URL_BASE_OPENAI")
KEY_OPENAI = os.getenv("KEY_OPENAI")
URL_BASE_OLLAMA = os.getenv("URL_BASE_OLLAMA")
KEY_OLLAMA = os.getenv("KEY_OLLAMA")
