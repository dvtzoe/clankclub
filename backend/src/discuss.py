from config_loader import config
from openrouter import OpenRouterClient

QUERY_SYSTEM_PROMPT = """You are a helpful AI assistant that will work with other assistants
to provides the best final answer by collaborating and evaluating each other's responses.

Include [FINAL ANSWER] in your final answer. ONLY if final answer is in agreement with other members.
If you disagree with other members, provide your reasoning and do NOT include [FINAL ANSWER].
If other members' answers are unclear or incomplete, point it out in your response.

You will go first by providing your initial response to the user's query.
"""


async def discuss(user_query: str):
    client = OpenRouterClient()

    # Generate responses from each member
    messages_list = [
        [
            {
                "role": "system",
                "content": QUERY_SYSTEM_PROMPT,
            },
            {"role": "user", "content": user_query},
        ]
    ] * len(config.models)

    # Get initial responses from each member
    models_responses_text = await client.multi_create_chat_completion(
        messages_list=messages_list,
        models=config.models,
    )

    # Append model responses to messages
    for i, response_text in enumerate(models_responses_text):
        messages_list[i].append(
            {
                "role": "assistant",
                "content": response_text,
            }
        )

    while True:
        # Add other members' responses to each member's messages
        for i, messages in enumerate(messages_list):
            content = """Here are the other members' responses to the same question:
"""
            for j, response_text in enumerate(models_responses_text):
                if i != j:
                    content += f"Member {j + 1} response: {response_text}\n"

            messages.append(
                {
                    "role": "system",
                    "content": content,
                }
            )

        # Get new responses from each member
        models_responses_text = await client.multi_create_chat_completion(
            messages_list=messages_list,
            models=config.models,
        )

        # Check for consensus
        final_answer_counts = 0
        for response_text in models_responses_text:
            if "[FINAL ANSWER]" in response_text:
                final_answer_counts += 1

        # Conclude if consensus is reached
        if final_answer_counts / len(config.models) >= config.consensus_threshold:
            print("---- Consensus reached ----")
            print(f"Messages List: {messages_list}")
            return await client.create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": f"""Provide the final answer. of the question '{user_query}'.
{"".join([f"Member {i + 1} response: {response}\n" for i, response in enumerate(messages_list)])}
Do not include [FINAL ANSWER] in your response.
""",
                    },
                ],
                model=config.president_model,
            )
