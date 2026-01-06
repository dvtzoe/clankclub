from schemas.message import Message, MessageNode, MessageTreeSchema, UniMessage


def message_tree_to_messages(
    message_tree: MessageTreeSchema,
) -> list[Message]:
    messages: list[Message] = []
    current_node = message_tree.nodes[message_tree.root]

    while True:
        messages.append(current_node.message)

        if not current_node.children:
            break
        current_node = message_tree.nodes[current_node.children[current_node.selected]]

    return messages


def messages_to_message_mapped(
    messages: list[Message],
    models: list[str],
) -> dict[str, list[UniMessage]]:
    message_mapped: dict[str, list[UniMessage]] = {}

    for model in models:
        message_mapped[model] = []

    for message in messages:
        print(f"message: {message}")
        if isinstance(message, dict):
            for model, uni_message in message.items():
                message_mapped[model].append(uni_message)
        else:
            print(f"Non-dict message: {message}")
            for model in models:
                print(f"Adding message to model {model}")
                message_mapped[model].append(message)

    return message_mapped


def messages_mapped_to_messages(
    messages_mapped: dict[str, list[UniMessage]],
) -> list[Message]:
    messages: list[Message] = []

    models = list(messages_mapped.keys())
    for i, sample_message in enumerate(next(iter(messages_mapped.values()), [])):
        if all(sample_message == messages_mapped[model][i] for model in models):
            messages.append(sample_message)
        else:
            multi_message: dict[str, UniMessage] = {}
            for model in models:
                multi_message[model] = messages_mapped[model][i]
            messages.append(multi_message)

    return messages


def messages_to_message_tree(
    messages: list[Message],
) -> MessageTreeSchema:
    if not messages:
        raise ValueError("Messages list is empty")

    first_node = MessageNode(message=messages[0])
    message_tree = MessageTreeSchema(root=first_node.id)
    message_tree.add_node(first_node)
    prev_node_id = first_node.id

    for message in messages[1:]:
        node = MessageNode(message=message)
        message_tree.add_node(node)
        message_tree.link(prev_node_id, node.id)
        prev_node_id = node.id

    return message_tree
