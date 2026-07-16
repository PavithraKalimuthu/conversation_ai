from database import memory_collection

def save_memory(user_id, text):

    memory_collection.insert_one({

        "user_id": user_id,

        "memory": text

    })


def get_memories(user_id):

    memories = memory_collection.find(

        {

            "user_id": user_id

        }

    )

    return [m["memory"] for m in memories]


def build_memory_context(user_id):

    memories = get_memories(user_id)

    if not memories:

        return ""

    return "\n".join(memories)