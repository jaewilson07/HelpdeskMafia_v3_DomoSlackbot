from fastapi import APIRouter

from src.services.openai import openai_agent, ChatRequest

# Initialize router
router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/call_openai_chat_completion")
async def call_openai_chat_completion(model: str, messages: list, temperature: float = 0.7, max_tokens: int = 150):
    """
    Implements an OpenAI chatbot for handling app messages.
    """
    chat_request = ChatRequest(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
    return await openai_agent.handle_chat_request(chat_request)
