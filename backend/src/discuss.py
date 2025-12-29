from typing import cast

from config_loader import config
from openrouter import OpenRouterClient
from schemas import (
    AssistantMessage,
    MessagesHistory,
    MessagesList,
    SystemMessage,
    UserMessage,
)

QUERY_SYSTEM_PROMPT = """You are a helpful AI assistant that will work with other assistants
to provides the best final answer by collaborating and evaluating each other's responses.

Include [FINAL ANSWER] in your final answer. If final answer is in agreement with other members.
If you disagree with other members, provide your reasoning
If other members' answers are unclear or incomplete, point it out in your response.

You must always include [FINAL ANSWER] in every response that you believe is the final answer.
or you already concluded that your answer is final.

You will go first by providing your initial response to the user's query.
"""


async def discuss(user_query: str):
    client = OpenRouterClient()

    # Generate responses from each member
    messages_list: MessagesList = cast(
        MessagesList,
        [
            [
                SystemMessage(content=QUERY_SYSTEM_PROMPT),
                UserMessage(content=user_query),
            ]
            for _ in config.models
        ],
    )

    messages_history: MessagesHistory = cast(
        MessagesHistory,
        [
            SystemMessage(content=QUERY_SYSTEM_PROMPT),
            UserMessage(content=user_query),
            [],
        ],
    )

    # Get initial responses from each member
    models_replies = await client.multi_create_chat_completion(
        messages_list=messages_list,
        models=config.models,
    )

    # Append model responses to messages
    for i, reply in enumerate(models_replies):
        messages_list[i].append(
            AssistantMessage(
                reply=reply,
            )
        )
        if isinstance(messages_history[2], list):
            messages_history[2].append(
                AssistantMessage(
                    reply=reply,
                )
            )

    while True:
        # Add other members' responses to each member's messages
        for i, messages in enumerate(messages_list):
            content = """Here are the other members' responses to the same question:
"""
            for j, reply in enumerate(models_replies):
                if i != j and reply:
                    content += f"Member {j + 1} response: {reply}\n"

            messages.append(SystemMessage(content=content))

        # Get new responses from each member
        models_replies = await client.multi_create_chat_completion(
            messages_list=messages_list,
            models=config.models,
        )

        print(f"New round of responses: {models_replies}")

        messages_history.append([])
        # Append new model responses to messages
        for i, reply in enumerate(models_replies):
            messages_list[i].append(AssistantMessage(reply=reply))
            if isinstance(messages_history[-1], list):
                messages_history[-1].append(
                    AssistantMessage(
                        reply=reply,
                    )
                )

        # Check for consensus
        final_answer_counts = 0
        for reply in models_replies:
            if (
                reply.choices[0].message.content is not None
                and "[FINAL ANSWER]" in reply.choices[0].message.content
            ):
                final_answer_counts += 1

        # for some reason sometimes llm returns nothing
        survivors_counts = 0
        if isinstance(messages_history[-1], list):
            for member_message in messages_history[-1]:
                if (
                    member_message
                    and member_message.content
                    and "[FINAL ANSWER]" in member_message.content
                ):
                    survivors_counts += 1

        # Conclude if consensus is reached
        print(f"History: {messages_history}")
        print(
            f"Agreement: {final_answer_counts} / {survivors_counts} (threshold: {config.consensus_threshold})"
        )
        if final_answer_counts / survivors_counts >= config.consensus_threshold:
            return (
                (
                    await client.create_chat_completion(
                        messages=[
                            SystemMessage(
                                content=f"""Provide the final answer. of the question '{
                                    user_query
                                }'.Do not reference other members in your final answer.{
                                    "\n".join(
                                        [
                                            "\n".join(
                                                [
                                                    f"Member {i + 1}: {member_message.content}\n"
                                                    if member_message
                                                    else ""
                                                    for i, member_message in enumerate(
                                                        history
                                                    )
                                                ]
                                            )
                                            if isinstance(history, list)
                                            else f"{history.role}: {history.content}\n"
                                            for history in messages_history[1:]
                                        ]
                                    )
                                }\n""",
                            )
                        ],
                        model=config.president_model,
                    )
                )
                .choices[0]
                .message.content
            )
