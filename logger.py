import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("ConversationalAI")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler(
    "logs/app.log",
    encoding="utf-8"
)

console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)