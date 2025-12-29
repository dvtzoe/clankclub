import asyncio
import os
from collections.abc import Iterable

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from config_loader import config
from schemas import Message, MessagesList


class OpenRouterClient:
    def __init__(self):
        load_dotenv()
        self.openai: AsyncOpenAI = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY") or config.openai_api_key,
            base_url=config.openai_base_url,
        )

    async def create_chat_completion(
        self,
        messages: Iterable[Message],
        model: str,
    ) -> ChatCompletion:
        response = await self.openai.chat.completions.create(
            model=model,
            messages=[message.to_openai() for message in messages],
        )
        # print(f"Messages: {messages}")
        print(f"Model: {model}")
        print(f"Response: {response.choices[0].message.content}")

        return response

    async def multi_create_chat_completion(
        self,
        messages_list: MessagesList,
        models: Iterable[str],
    ) -> list[ChatCompletion]:
        tasks = [
            self.create_chat_completion(messages=messages, model=model)
            for messages, model in zip(messages_list, models)
        ]

        responses = await asyncio.gather(*tasks)
        return responses
