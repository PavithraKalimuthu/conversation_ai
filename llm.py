from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL_NAME
)

from prompts import SYSTEM_PROMPT

client = Groq(api_key=GROQ_API_KEY)


def build_messages(
    query,
    history=None,
    memory="",
    rag=""
):

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Previous conversation
    messages.extend(history)

    # Build user context
    context = ""

    if memory:
        context += (
            "### User Memory ###\n"
            f"{memory}\n\n"
        )

    if rag:
        context += (
            "### Knowledge Base ###\n"
            f"{rag}\n\n"
        )

    context += f"""
### User Question ###
{query}

Instructions:

1. If Knowledge Base is provided, answer using it first.
2. If User Memory helps answer the question, use it.
3. If both Knowledge Base and Memory are available, combine them naturally.
4. If the answer is NOT present in the Knowledge Base or Memory, clearly say you couldn't find it.
5. Never claim that the user did not upload a document if Knowledge Base exists.
6. Never invent information.
7. Use your general knowledge ONLY when no relevant Knowledge Base is available.
8. Keep answers concise, accurate and conversational.
"""

    messages.append(
        {
            "role": "user",
            "content": context
        }
    )

    return messages


def generate_response(
    query,
    history=None,
    memory="",
    rag=""
):

    messages = build_messages(
        query=query,
        history=history,
        memory=memory,
        rag=rag
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=1024
    )

    return response.choices[0].message.content


def stream_response(
    query,
    history=None,
    memory="",
    rag=""
):

    messages = build_messages(
        query=query,
        history=history,
        memory=memory,
        rag=rag
    )

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=1024,
        stream=True
    )

    for chunk in completion:

        if chunk.choices:

            token = chunk.choices[0].delta.content

            if token:

                yield token