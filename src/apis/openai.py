from fastapi import APIRouter

from utils.pydantic_agent_generator import generate_pydantic_agent, generate_agent_dependencies, generate_model

# Initialize router
router = APIRouter(prefix="/ai", tags=["ai"])

openai_agent = generate_pydantic_agent(system_prompt="You are a helpful AI assistant for OpenAI API requests.")
openai_model = generate_model()
agent_deps = generate_agent_dependencies()


@router.post("/call_openai_chat_completion")
async def call_openai_chat_completion(messages: list):
    """
    Implements an OpenAI chatbot for handling app messages.
    """

    return await openai_agent.run(user_prompt=messages, model=openai_model, deps=agent_deps)
