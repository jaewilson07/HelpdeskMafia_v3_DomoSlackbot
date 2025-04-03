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


def generate_model(model_name: str = openai_model_name, provider="openai") -> OpenAIModel:
    """Generates an OpenAIModel instance with the specified model name."""
    return OpenAIModel(
        model_name=model_name,
        provider=provider,
        api_key=openai_api_key,  # Add the missing api_key parameter
    )


def generate_pydantic_agent(retries=1, system_prompt="you are helpful ai agent"):
    return PydanticAgent(
        model=generate_model(),
        system_prompt=system_prompt,
        deps_type=PydanticAIDependencies,
        retries=retries,
    )


def generate_agent_dependencies() -> PydanticAIDependencies:

    return PydanticAIDependencies(openai=AsyncOpenAI(api_key=openai_api_key))
