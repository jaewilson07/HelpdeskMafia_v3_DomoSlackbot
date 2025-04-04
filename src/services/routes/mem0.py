import os
from mem0 import Memory
from src.utils.supabase import generate_supabase_conection_string


openai_api_key = os.environ["OPENAI_API_KEY"]
openai_model = os.environ["OPENAI_MODEL"]

neo4j_password = os.environ["NEO4J_PASSWORD"]
neo4j_user = os.environ["NEO4J_USERNAME"]
neo4j_uri = os.environ["NEO4J_URI"]

supabase_password = os.environ["SUPABASE_PASSWORD"]
supabase_connection_string = os.environ["SUPABASE_CONNECTION_STRING"]

supabase_connection_string = generate_supabase_conection_string(supabase_connection_string, supabase_password)


def generate_mem0_config() -> dict:
    """Generate the configuration dictionary for Memory."""
    return {
        "llm": {
            "provider": "openai",
            "config": {
                "api_key": openai_api_key,
                "model": openai_model,
                "temperature": 0.7,
                "max_tokens": 2000,
            },
        },
        "graph_store": {
            "provider": "neo4j",
            "config": {"url": neo4j_uri, "username": neo4j_user, "password": neo4j_password},
        },
        "vector_store": {
            "provider": "supabase",
            "config": {
                "connection_string": supabase_connection_string,
                "collection_name": "memories",
                "index_method": "hnsw",  # Optional: defaults to "auto"
                "index_measure": "cosine_distance",  # Optional: defaults to "cosine_distance"
            },
        },
    }


memory: Memory = Memory.from_config(generate_mem0_config())


async def get_relevant_user_memories(message, user_id, top_k=5):
    return memory.search(
        query=message,
        user_id=user_id,
        limit=top_k,
    )


async def add_user_memories(user_id, messages):
    """
    Adds a new memory for the user.

    :param user_id: The ID of the user.
    :param message: The message to be stored as a memory.
    :param metadata: Optional metadata associated with the memory.
    """
    return memory.add(user_id=user_id, messages=messages)
