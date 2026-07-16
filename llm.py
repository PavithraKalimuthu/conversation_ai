from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL_NAME
)

from prompts import SYSTEM_PROMPT

client = Groq(
    api_key=GROQ_API_KEY
)


def build_messages(

    query,

    history=[],

    memory="",

    rag=""
):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    if memory:

        messages.append(

            {

                "role": "system",

                "content": f"User Memory:\n{memory}"

            }

        )

    if rag:

        messages.append(

            {

                "role": "system",

                "content": f"Knowledge Base:\n{rag}"

            }

        )

    messages.extend(history)

    messages.append(

        {

            "role": "user",

            "content": query

        }

    )

    return messages


def generate_response(

    query,

    history=[],

    memory="",

    rag=""

):

    messages = build_messages(

        query,

        history,

        memory,

        rag

    )

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=messages,

        temperature=0.3,

        max_tokens=1024

    )

    return response.choices[0].message.content


def stream_response(

    query,

    history=[],

    memory="",

    rag=""

):

    messages = build_messages(

        query,

        history,

        memory,

        rag

    )

    completion = client.chat.completions.create(

        model=MODEL_NAME,

        messages=messages,

        temperature=0.3,

        max_tokens=1024,

        stream=True

    )

    for chunk in completion:

        if chunk.choices:

            token = chunk.choices[0].delta.content

            if token:

                yield token