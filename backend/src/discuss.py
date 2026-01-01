from uuid import UUID

from config_loader import config
from openrouter import OpenRouterClient
from schemas import (
    AssistantMessage,
    Message,
    MessagesHistoryNode,
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

    # Generate responses from each member and map to messages list and history
    initial_system_message = SystemMessage(content=QUERY_SYSTEM_PROMPT)
    initial_user_message = UserMessage(content=user_query)

    messages_list: list[list[Message]] = [
        [
            initial_system_message,
            initial_user_message,
        ]
        for _ in config.models
    ]

    initial_user_message_node = MessagesHistoryNode(
        message_id=initial_user_message.id,
    )

    initial_system_message_node = MessagesHistoryNode(
        message_id=initial_system_message.id,
        next_node=[initial_user_message_node.id],
    )

    messages_history: list[MessagesHistoryNode] = [
        initial_system_message_node,
        initial_user_message_node,
    ]

    # Get initial responses from each member
    models_replies = await client.multi_create_chat_completion(
        messages_list=messages_list,
        models=config.models,
    )

    # Append model responses to messages
    message_ids = []
    for i, reply in enumerate(models_replies):
        message = AssistantMessage(raw=reply)
        messages_list[i].append(message)
        message_ids.append(message.id)
    message_history_node = MessagesHistoryNode(
        message_id=message_ids,
    )
    messages_history[-1].next_node = [message_history_node.id]
    messages_history.append(message_history_node)

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

        # Append new model responses to messages
        message_ids: list[UUID] = []
        for i, reply in enumerate(models_replies):
            message = AssistantMessage(raw=reply)
            messages_list[i].append(message)
            message_ids.append(message.id)
        message_history_node = MessagesHistoryNode(
            message_id=message_ids,
        )
        messages_history[-1].next_node = [message_history_node.id]
        messages_history.append(message_history_node)

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
        for member_message in messages_list[:][-1]:
            if (
                member_message
                and member_message.content
                and "[FINAL ANSWER]" in member_message.content
            ):
                survivors_counts += 1

        # Conclude if consensus is reached
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
                                                        messages
                                                    )
                                                ]
                                            )
                                            if messages[0].role == "assistant"
                                            else f"{messages[0].role}: {messages[0].content}\n"
                                            for messages in messages_list[:][1:]
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
