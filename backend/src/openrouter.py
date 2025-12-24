from collections.abc import Iterable
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import cast
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam


class OpenRouterClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        self.openai: OpenAI = OpenAI(api_key=api_key)

    def create_chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
    ) -> ChatCompletion:
        response = self.openai.chat.completions.create(
            model=model,
            messages=cast(Iterable[ChatCompletionMessageParam], messages),
        )
        return response
