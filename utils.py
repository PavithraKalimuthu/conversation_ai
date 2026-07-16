import uuid
import re


def generate_uuid():
    return str(uuid.uuid4())


def clean_text(text: str):

    if not text:
        return ""

    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    return text


def history_to_messages(history):

    messages = []

    for row in history:

        messages.append(
            {
                "role": row["role"],
                "content": row["message"]
            }
        )

    return messages


def trim_history(history, limit=10):

    if len(history) <= limit:
        return history

    return history[-limit:]


def build_context(memory="", rag=""):

    context = ""

    if memory:

        context += f"\nUser Memory:\n{memory}\n"

    if rag:

        context += f"\nKnowledge Base:\n{rag}\n"

    return context