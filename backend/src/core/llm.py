import asyncio
import os
from collections.abc import Iterable

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from core.config import Config
from schemas import Message

load_dotenv()


class LLM:
    openai: AsyncOpenAI = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY") or Config.get().openai_api_key,
        base_url=Config.get().openai_base_url,
    )

    @classmethod
    async def create_chat_completion(
        cls,
        messages: Iterable[Message],
        model: str,
    ) -> ChatCompletion:
        response = await cls.openai.chat.completions.create(
            model=model,
            messages=[message.to_openai() for message in messages],
        )
        # print(f"Messages: {messages}")
        print(f"Model: {model}")
        print(f"Response: {response.choices[0].message.content}")

        return response

    @classmethod
    async def multi_create_chat_completion(
        cls,
        messages_list: dict[str, list[Message]],
        models: list[str],
    ) -> dict[str, ChatCompletion]:
        tasks = [
            cls.create_chat_completion(messages=messages, model=model)
            for messages, model in zip(messages_list.values(), models)
        ]

        responses = await asyncio.gather(*tasks)

        result = {}

        for model, response in zip(models, responses):
            result[model] = response

        return result
