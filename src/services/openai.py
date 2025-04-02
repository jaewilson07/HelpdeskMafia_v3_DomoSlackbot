"""service for interacting with openai's api"""

from pydantic_ai import RunContext

import openai

from src.utils.pydantic import generate_pydantic_agent, PydanticAIDependencies, ChatRequest

openai_agent = generate_pydantic_agent()


@openai_agent.tool
async def call_chat_completion(
    ctx: RunContext[PydanticAIDependencies], messages: list, temperature: float = 0.7, max_tokens: int = 150
):
    """
    Calls OpenAI's chat completion API using the openai library.
    """
    try:
        response = await ctx.deps.openai.ChatCompletion.acreate(
            messages=messages, temperature=temperature, max_tokens=max_tokens
        )
        return response

    except openai.error.OpenAIError as e:
        return {"error": str(e)}
