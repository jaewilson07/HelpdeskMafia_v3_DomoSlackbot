from fastapi import APIRouter
from pydantic_ai import OpenAISchema

# Initialize router
router = APIRouter(prefix="/ai", tags=["ai"])


# Define the OpenAI schema using pydantic-ai
class ChatRequest(OpenAISchema):
    model: str
    messages: list
    temperature: float = 0.7
    max_tokens: int = 150


# Create OpenAI route using pydantic-ai
@router.post("/chat-completion")
async def chat_completion(request: ChatRequest):
    return await request.openai_chat_completion()
