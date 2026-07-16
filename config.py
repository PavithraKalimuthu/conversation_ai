import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = "conversation_ai"

CHROMA_PATH = os.getenv("CHROMA_PATH")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

UPLOAD_FOLDER = "uploads"
KNOWLEDGE_FOLDER = "knowledge"
LOG_FOLDER = "logs"