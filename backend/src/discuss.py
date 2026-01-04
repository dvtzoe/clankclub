from core.config import Config
from openrouter import OpenRouterClient
from schemas.message import (
    AssistantMessage,
    Message,
    MessageNode,
    MessageTreeSchema,
    MultiModelMessage,
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
    config = Config.get()

    # Generate responses from each member and map to messages list and history
    initial_system_message = SystemMessage(content=QUERY_SYSTEM_PROMPT)
    initial_user_message = UserMessage(content=user_query)

    messages_list: dict[str, list[Message]] = {}
    for i, model in enumerate(config.models):
        messages_list[model] = [
            initial_system_message,
            initial_user_message,
        ]

    # Initialize message history tree
    first_node = MessageNode(message=initial_system_message)
    current_node = MessageNode(message=initial_user_message)

    messages_tree = (
        MessageTreeSchema(root=first_node.id)
        .add_node(first_node)
        .add_node(current_node)
        .link(first_node.id, current_node.id)
    )
    # Get initial responses from each member
    models_replies = await client.multi_create_chat_completion(
        messages_list=messages_list,
        models=config.models,
    )

    # Append model responses to messages
    replies_message: MultiModelMessage = {}
    for model, reply in models_replies.items():
        message = AssistantMessage(raw=reply)
        messages_list[model].append(message)
        replies_message[model] = message
    previous_id = current_node.id
    current_node = MessageNode(message=replies_message)
    messages_tree.add_node(current_node).link(previous_id, current_node.id)

    while True:
        # Add other members' responses to each member's messages
        for model_from_list, messages in messages_list.items():
            content = """Here are the other members' responses to the same question:
"""
            for i, (model_reply, reply) in enumerate(models_replies.items()):
                if model_from_list != model_reply and reply:
                    content += f"Member {i + 1} response: {reply}\n"

            messages.append(SystemMessage(content=content))

        # Get new responses from each member
        models_replies = await client.multi_create_chat_completion(
            messages_list=messages_list,
            models=config.models,
        )

        print(f"New round of responses: {models_replies}")

        # Append new model responses to messages
        replies_message = {}
        for model, reply in models_replies.items():
            message = AssistantMessage(raw=reply)
            messages_list[model].append(message)
            replies_message[model] = message
        previous_id = current_node.id
        current_node = MessageNode(message=replies_message)
        messages_tree.add_node(current_node).link(previous_id, current_node.id)

        # Check for consensus
        final_answer_counts = 0
        for reply in models_replies.values():
            if (
                reply.choices[0].message.content is not None
                and "[FINAL ANSWER]" in reply.choices[0].message.content
            ):
                final_answer_counts += 1

        # for some reason sometimes llm returns nothing
        survivors_counts = 0
        for member_message in list(messages_list.values())[:][-1]:
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
                                }'.Do not reference other members 
                                and do not include [FINAL ANSWER] in your final answer{
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
                                            for messages in list(
                                                messages_list.values()
                                            )[:][1:]
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
