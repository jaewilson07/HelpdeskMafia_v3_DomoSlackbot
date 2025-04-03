"""
This module integrates with OpenAI's API to provide tools for summarizing
chat messages and generating AI-powered responses.

It uses the `pydantic-ai` library to simplify schema-based AI interactions.
"""

from utils.pydantic_agent_generator import (
    generate_pydantic_agent,
    PydanticAIDependencies,
    generate_agent_dependencies,
    generate_model,
)

from pydantic_ai import RunContext

from openai import OpenAIError
import json
from typing import List
import logging

logger = logging.getLogger(__name__)
openai_agent = generate_pydantic_agent()


@openai_agent.tool
async def call_chat_completion(ctx: RunContext[PydanticAIDependencies], messages: List[dict]):
    """
    Calls OpenAI's chat completion API and returns a response.

    Args:
        ctx (RunContext[PydanticAIDependencies]): The context holding dependencies, including an OpenAI client.
        messages (List[dict]): A list of message dictionaries containing 'role' and 'content'.

    Returns:
        dict: A response from OpenAI's chat completion API or an error message.
    """
    try:
        response = await ctx.deps.openai.chat.completions.create(messages=messages)
        return response
    except OpenAIError as e:
        print(e)
        return {"error": str(e)}


@openai_agent.tool
async def summarize_text(
    ctx: RunContext[PydanticAIDependencies],
    messages: list,
):
    """
    Summarizes chat messages using OpenAI's completion endpoint.

    Args:
        ctx (RunContext[PydanticAIDependencies]): The context holding dependencies for interacting with OpenAI.
        messages (list): A list of dictionaries representing individual chat messages to summarize.

    Returns:
        dict: A response containing the summarized text or an error message.
    """

    system_prompt = """You are a helpful assistant that summarizes chat histories.  Format the response as in slack-compatible markdown format.
    sample response:
    ## Channel activity
    < users who joined>

    ## Discussion Topics
    < short summary information, user(s) involved, link to conversation
    
    ## Actions or Agreements
    < any action items or agreements made during the discussion, including who is responsible and due dates if mentioned, link to conversation >

    ## Bugs or Problems Identified
    < any bugs or problems identified during the discussion, including who reported them and any follow-up actions required, link to conversation >
    """

    user_content = "Provide a very detailed summary of the following chat history:\n\n" + json.dumps(messages)

    if not ctx.deps.openai:
        raise ValueError("OpenAI client is not initialized in the context dependencies.")

    try:
        return await ctx.deps.openai.chat.completions.create(
            messages=[
                {
                    "prompt": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_content},
            ],
        )

    except OpenAIError as e:
        logger.error("OpenAI API error: %s", e)
        return {"error": str(e)}


def format_message(messages: List[dict]) -> List[dict]:
    """
    Maps over messages and retains only fields of interest.

    Args:
        messages (List[dict]): A list of message dictionaries.

    Returns:
        List[dict]: A list of formatted message dictionaries.
    """
    return [
        {
            "user_id": msg.get("user_id") or msg.get("user"),  # Fallback to 'user' if 'user_id' is not present
            "user_name": msg.get("user_name") or msg.get("username"),  # Fallback to 'username' if 'user_name' is not present
            "text": msg.get("text").strip(),
            "timestamp": msg.get("ts"),
        }
        for msg in messages
    ]


openai_agent = generate_pydantic_agent(
    system_prompt="""you are a senior executive assistant who excels at summarizing chat conversations"""
)

agent_deps = generate_agent_dependencies()
openai_model = generate_model()


async def summarize_chat_messages(
    messages: List[dict],
):
    """
    Summarizes chat messages using OpenAI's chat completion API.

    Args:
        messages (List[dict]): A list of message dictionaries to summarize.

    Returns:
        str: The summarized text or an error message.
    """
    if not messages:
        return "No messages to summarize."

    # Generate summary using OpenAI
    user_prompt = f"Summarize the following chat messages: {json.dumps(format_message(messages))}"

    return await openai_agent.run(user_prompt=user_prompt, deps=agent_deps, model=openai_model)
