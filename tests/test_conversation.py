from src.barabasz.parsers import ConversationMessage, Conversation, Role


def test_Conversation_add_message():
    test_conversation = Conversation()
    test_conversation.add_message(
        ConversationMessage(role=Role.system, message="First message")
    )
    assert len(test_conversation.history) == 1


def test_Conversation_reset():
    test_conversation = Conversation()
    test_conversation.add_message(
        ConversationMessage(role=Role.system, message="First message")
    )
    test_conversation.reset()
    assert len(test_conversation.history) == 0


def test_Conversation_parsing_to_chat_format():
    test_conversation = Conversation()
    test_conversation.add_message(
        ConversationMessage(role=Role.system, message="First message")
    )

    assert test_conversation.get_conversation_in_chat_format() == [
        {"role": "system", "content": "First message"}
    ]
