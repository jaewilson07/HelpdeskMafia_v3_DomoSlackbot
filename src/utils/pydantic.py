from dataclasses import dataclass

from openai import AsyncOpenAI

from pydantic_ai import Agent as PydanticAgent
from pydantic_ai.models.openai import OpenAIModel

import os


openai_api_key = os.environ["OPENAI_API_KEY"]
openai_model_name = os.environ["OPENAI_MODEL"]


@dataclass
class PydanticAIDependencies:
    openai: AsyncOpenAI


@dataclass
class ChatRequest:
    messages: list
    temperature: float = 0
    max_tokens: int = 200


openai_model = OpenAIModel(
    model_name=openai_model_name,
    provider="openai",
    # api_key=openai_api_key,
)


def generate_pydantic_agent(retries=1, system_prompt="you are helpful ai agent"):
    return PydanticAgent(
        model=openai_model,
        system_prompt=system_prompt,
        deps_type=PydanticAIDependencies,
        retries=retries,
    )
