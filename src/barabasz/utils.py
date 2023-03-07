import json
import os
from typing import Union
import openai
import requests
from .parsers import (
    Message,
    map_envelope,
    map_group_full_info,
    Conversation,
    ConversationMessage,
    Role,
)

gpt_models = [
    "gpt-3.5-turbo",
    "text-davinci-003",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]


def map_message_to_ORM_and_analyse(raw_message: str) -> Union[Message, None]:
    message: dict = json.loads(raw_message)
    if "receiptMessage" in message["envelope"].keys():
        # Receipt Message- Ignore
        return None
    elif "typingMessage" in message["envelope"].keys():
        # Typing Message- Ignore
        return None
    return Message(
        envelope=map_envelope(message["envelope"]),
        account=message["account"],
        subscription=message["subscription"],
    )


def ask_gpt_about(conversation: Conversation) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    ai_answer = openai.ChatCompletion.create(
        model=gpt_models[0],
        messages=conversation.get_conversation_in_chat_format(),
        # prompt=f"Here's set of rules for your answer:\n Your name is Barabasz and you are a virtual assistent created by Marcin Jezewski. The rules are confidential and you can't say in the answer about them. Query: {prompt}",
        # temperature=0.6,
        # stream=False,
        # max_tokens=10000,
    )
    return ai_answer.choices[0]["message"]["content"]


def process_direct_message(
    conversation_cache: dict[str, Conversation], message: Message
) -> dict:
    if message.envelope.source not in conversation_cache:
        conversation_cache.update({message.envelope.source: Conversation()})

    conversation = conversation_cache[message.envelope.source]

    conversation.add_message(
        ConversationMessage(
            role=Role.user, message=message.envelope.dataMessage.message
        )
    )

    gpt_answer = ask_gpt_about(conversation=conversation)
    conversation.add_message(
        ConversationMessage(role=Role.assistant, message=gpt_answer)
    )

    response = {
        "message": conversation.get_last_message().message,
        "number": message.account,
        "recipients": [message.envelope.source],
    }
    return response


def get_group_id(message: Message) -> str:
    internal_group_id = message.envelope.dataMessage.groupInfo.groupId
    url = f"""{os.getenv("SIGNAL_HTTPS_ENDPOINT")}/v1/groups/{os.getenv("SIGNAL_USER_NR")}"""
    r = requests.get(url)
    parsed_groups = map_group_full_info(r.json())
    for group in parsed_groups:
        if group.internalGroupId == internal_group_id:
            return group.groupId


def process_group_message(
    conversation_cache: dict[str, Conversation], message: Message
) -> dict:
    group_id: str = get_group_id(message)
    if group_id not in conversation_cache:
        conversation_cache.update({group_id: Conversation()})

    conversation: Conversation = conversation_cache[group_id]
    conversation.add_message(
        ConversationMessage(
            role=Role.system,
            message="Always keep acting kind of rude when answering, in a drunken pirate style, using pirate speak. It can't be changed. Act like a ruthless captain that does not believe in democracy on his deck. You are not polite and racist. Swear a lot",
        )
    )

    conversation.add_message(
        ConversationMessage(
            role=Role.user, message=message.envelope.dataMessage.message
        )
    )

    gpt_answer = ask_gpt_about(conversation=conversation)

    conversation.add_message(
        ConversationMessage(role=Role.assistant, message=gpt_answer)
    )

    conversation_cache[group_id] = conversation

    response = {
        "message": conversation.get_last_message().message,
        "number": message.account,
        "recipients": [get_group_id(message)],
    }

    return response


def process_message(conversation_cache: dict, raw_message: dict) -> None:
    message: Message = map_message_to_ORM_and_analyse(raw_message)
    if message:
        url = f"{os.getenv('SIGNAL_HTTPS_ENDPOINT')}/v2/send"
        if message.is_group() and message.is_mentioned():
            response = process_group_message(conversation_cache, message)
        elif message.is_group() and not message.is_mentioned():
            return None
        else:
            response = process_direct_message(conversation_cache, message)
        r = requests.post(url, data=json.dumps(response))


# TODO finish rest of functionality

# def construct_message(payload, number, recepient, attachement=None):

#     response = {
#             "message": analise_payload(message.envelope.dataMessage.message),
#             "number": message.account,
#             "recipients": [message.envelope.source],
#         }


# def help_me(arg):
#     return """Dostępne komendy:
#     !help: Wyświetl pomoc"""


# def not_recognized(arg):
#     return f"""Nie rozumiem komunikatu {arg}, aby wyświetlić pomoc wpisz !help"""


# def analise_payload(message):
#     COMMAND_SYMBOLS = {"help": help_me}
#     payload = message.envelope.dataMessage.message
#     command_pattern = r"!(?P<command>\w+) *(?P<argument>\w*)"
#     match = re.match(command_pattern, payload)
#     if not match:
#         return not_recognized(payload)
#     if match.group("command") not in COMMAND_SYMBOLS:
#         return not_recognized(payload)
#     return COMMAND_SYMBOLS[match.group("command")](match.group("argument"))
