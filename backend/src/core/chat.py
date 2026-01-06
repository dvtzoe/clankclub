from uuid import UUID

from openai.types.chat import ChatCompletion
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import Config
from core.llm import LLM
from models.session import SessionModel
from schemas.message import (
    AssistantMessage,
    Message,
    MessageNode,
    MessageTreeSchema,
    ResponseMessage,
    SystemMessage,
    UniMessage,
    UserMessage,
)
from schemas.session import SessionSchema
from utils.message_cast import message_tree_to_messages, messages_to_message_mapped

QUERY_SYSTEM_PROMPT = """You are a helpful AI assistant that will work with other assistants
to provides the best final answer by collaborating and evaluating each other's responses.

Include [FINAL ANSWER] in your final answer. If final answer is in agreement with other members.
If you disagree with other members, provide your reasoning
If other members' answers are unclear or incomplete, point it out in your response.

You must always include [FINAL ANSWER] in every response that you believe is the final answer.
or you already concluded that your answer is final.

You will go first by providing your initial response to the user's query.
"""


async def chat(
    user_input: str,
    session_id: UUID | None = None,
    db_session: AsyncSession | None = None,
) -> str:
    user_message = UserMessage(content=user_input)
    user_message_node = MessageNode(message=user_message)
    message_tree: MessageTreeSchema
    if session_id and db_session:
        stmt = select(SessionModel).where(SessionModel.id == session_id)
        result = await db_session.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            raise ValueError("Session not found")

        message_tree = MessageTreeSchema(**session.message_tree)
        message_tree.add_node(user_message_node)
        message_tree.link(message_tree.end().id, user_message_node.id)
    else:
        message_tree = MessageTreeSchema(root=user_message_node.id)
        message_tree.add_node(user_message_node)

        session_schema = SessionSchema(message_tree=message_tree)
        session = SessionModel(**session_schema.model_dump(mode="json"))
        session_id = session_id or session.id
        if db_session:
            db_session.add(session)
            await db_session.commit()
    messages: list[Message] = message_tree_to_messages(message_tree)

    messages.insert(0, SystemMessage(content=QUERY_SYSTEM_PROMPT))

    discuss_result = await discuss(messages)

    if session_id and db_session:
        response_message = MessageNode(message=ResponseMessage(raw=discuss_result))
        message_tree.add_node(response_message)
        message_tree.link(message_tree.end().id, response_message.id)

        stmt = (
            insert(SessionModel)
            .values(
                id=session_id,
                message_tree=message_tree.model_dump(mode="json"),
                title=session.title,
            )
            .on_conflict_do_update(
                index_elements=[SessionModel.id],
                set_=dict(
                    message_tree=message_tree.model_dump(mode="json"),
                ),
            )
        )

        await db_session.execute(stmt)
        await db_session.commit()

    return discuss_result.choices[0].message.content or ""


async def ask(
    messages: list[Message],
) -> ChatCompletion:
    config = Config.get()

    flat_messages: list[UniMessage] = []
    for message in messages:
        if isinstance(message, dict):
            role = next(iter(message.values())).role
            content = "\n".join(
                [
                    f"Anonymous: {uni_message.content}"
                    for uni_message in message.values()
                ]
            )
            if role == "user":
                flat_messages.append(UserMessage(content=content))
            elif role == "assistant":
                flat_messages.append(AssistantMessage(content=content))
            elif role == "system":
                flat_messages.append(SystemMessage(content=content))
        else:
            flat_messages.append(message)

    response = await LLM.create_chat_completion(
        messages=flat_messages,
        model=config.president_model,
    )

    return response


async def discuss(
    messages: list[Message],
) -> ChatCompletion:
    config = Config.get()

    print(f"messages: {messages}")
    messages_mapped = messages_to_message_mapped(messages, config.models)
    print(f"messages_mapped: {messages_mapped}")
    print(config.models)

    if isinstance(messages[-1], dict):
        raise ValueError(
            "Last message must be a user message with content (not a dict)"
        )
    user_query = messages[-1].content

    # Get initial responses from each member
    models_replies = await LLM.multi_create_chat_completion(
        messages_mapped=messages_mapped,
        models=config.models,
    )

    # Append model responses to messages
    for model, reply in models_replies.items():
        message = ResponseMessage(raw=reply)
        messages_mapped[model].append(message)

    while True:
        # Add other members' responses to each member's messages
        for model_from_list, unimessages in messages_mapped.items():
            content = """Here are the other members' responses to the same question:
"""
            for i, (model_reply, reply) in enumerate(models_replies.items()):
                if model_from_list != model_reply and reply:
                    content += f"Member {i + 1} response: {reply}\n"

            unimessages.append(SystemMessage(content=content))

        # Get new responses from each member
        models_replies = await LLM.multi_create_chat_completion(
            messages_mapped=messages_mapped,
            models=config.models,
        )

        print(f"New round of responses: {models_replies}")

        # Append new model responses to messages
        for model, reply in models_replies.items():
            message = ResponseMessage(raw=reply)
            messages_mapped[model].append(message)

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
        for member_message in list(messages_mapped.values())[:][-1]:
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
            result = await LLM.create_chat_completion(
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
                                            for i, member_message in enumerate(messages)
                                        ]
                                    )
                                    if messages[0].role == "assistant"
                                    else f"{messages[0].role}: {messages[0].content}\n"
                                    for messages in list(messages_mapped.values())[:][
                                        1:
                                    ]
                                ]
                            )
                        }\n""",
                    )
                ],
                model=config.president_model,
            )
            return result
