import asyncio
import os
from collections.abc import Iterable
from typing import cast

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from config_loader import config


class OpenRouterClient:
    def __init__(self):
        load_dotenv()
        self.openai: AsyncOpenAI = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY") or config.openai_api_key,
            base_url=config.openai_base_url,
        )

    async def create_chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
    ) -> str:
        response = await self.openai.chat.completions.create(
            model=model,
            messages=cast(Iterable[ChatCompletionMessageParam], messages),
        )

        print(f"---- {model} ----")
        print(f"response content: {response.choices[0].message.content}")
        print("---------------")

        return response.choices[0].message.content or ""

    async def multi_create_chat_completion(
        self,
        messages_list: list[list[dict[str, str]]],
        models: list[str],
    ) -> list[str]:
        tasks = [
            self.create_chat_completion(messages=messages, model=model)
            for messages, model in zip(messages_list, models)
        ]

        responses = await asyncio.gather(*tasks)
        return responses
