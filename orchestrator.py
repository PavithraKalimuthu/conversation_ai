"""
orchestrator.py
"""

from database import (
    get_mysql_connection
)

from memory_manager import (
    save_memory,
    build_memory_context
)

from rag_manager import (
    retrieve_context
)

from llm import (
    stream_response
)

from utils import (
    history_to_messages,
    generate_uuid
)


# --------------------------------------
# Load Chat History
# --------------------------------------

def load_history(user_id):

    conn = get_mysql_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role,message
        FROM chat_history
        WHERE user_id=%s
        ORDER BY created_at ASC
        """,
        (user_id,)
    )

    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return history


# --------------------------------------
# Save Chat
# --------------------------------------

def save_chat(user_id, role, message):

    conn = get_mysql_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (user_id,role,message)
        VALUES(%s,%s,%s)
        """,
        (
            user_id,
            role,
            message
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


# --------------------------------------
# Chat
# --------------------------------------

def chat(user_id, query):

    history = load_history(user_id)

    history_messages = history_to_messages(history)

    memory = build_memory_context(user_id)

    try:
        rag = retrieve_context(
            user_id,
            query
        )
    except Exception:
        rag = ""

    save_chat(
        user_id,
        "user",
        query
    )

    full_response = ""

    for token in stream_response(

        query=query,

        history=history_messages,

        memory=memory,

        rag=rag

    ):

        full_response += token

        yield token

    save_chat(

        user_id,

        "assistant",

        full_response

    )

    save_memory(

        user_id,

        query

    )


# --------------------------------------
# Get History
# --------------------------------------

def get_history(user_id):

    return load_history(user_id)