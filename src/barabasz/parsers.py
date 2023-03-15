import dataclasses
import re
from uuid import UUID
from typing import List, Union
from enum import Enum
from .SETTINGS import MAIN_ADMIN_PROMPT


@dataclasses.dataclass
class GroupInfo:
    groupId: str
    groupType: str


@dataclasses.dataclass
class Mention:
    name: str
    number: str
    uuid: UUID
    start: int
    length: int


@dataclasses.dataclass
class DataMessage:
    timestamp: int
    message: str
    expiresInSeconds: int
    viewOnce: bool
    groupInfo: Union[GroupInfo, None] = None
    mentions: list[Mention] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Envelope:
    source: str
    sourceNumber: str
    sourceUuid: UUID
    sourceName: str
    sourceDevice: int
    timestamp: int
    dataMessage: DataMessage


@dataclasses.dataclass
class Message:
    envelope: Envelope
    account: str
    subscription: int

    def is_group(self):
        return True if self.envelope.dataMessage.groupInfo else False

    def is_mentioned(self):
        return True if self.envelope.dataMessage.mentions else False

    def is_meta(self):
        match = re.match(
            r".*!(?P<command>\w+) *(?P<rest>.*)", self.envelope.dataMessage.message
        )
        return True if match else False


@dataclasses.dataclass
class GroupFullInfo:
    """Class used to contain information about groups, when listing them from API"""

    admins: List[str]
    blocked: bool
    groupId: str
    internalGroupId: str
    inviteLink: str
    members: List[str]
    name: str
    pending_invites: List[str]
    pending_requests: List[str]


def map_group_full_info(raw_info: list) -> List[GroupFullInfo]:
    return [
        GroupFullInfo(
            admins=x["admins"],
            blocked=x["blocked"],
            groupId=x["id"],
            internalGroupId=x["internal_id"],
            inviteLink=x["invite_link"],
            members=x["members"],
            name=x["name"],
            pending_invites=x["pending_invites"],
            pending_requests=x["pending_requests"],
        )
        for x in raw_info
    ]


def map_dataMessage(data_message):
    datamessage = DataMessage(
        timestamp=data_message["timestamp"],
        message=data_message["message"],
        expiresInSeconds=data_message["expiresInSeconds"],
        viewOnce=data_message["viewOnce"],
    )
    if "groupInfo" in data_message:
        datamessage.groupInfo = GroupInfo(
            groupId=data_message["groupInfo"]["groupId"],
            groupType=data_message["groupInfo"]["type"],
        )
    if "mentions" in data_message:
        for mention in data_message["mentions"]:
            datamessage.mentions.append(
                Mention(
                    name=mention["name"],
                    number=mention["number"],
                    uuid=UUID(mention["uuid"]),
                    start=mention["start"],
                    length=mention["length"],
                )
            )
    return datamessage


def map_envelope(envelope):
    return Envelope(
        source=envelope["source"],
        sourceNumber=envelope["sourceNumber"],
        sourceUuid=UUID(envelope["sourceUuid"]),
        sourceName=envelope["sourceName"],
        sourceDevice=envelope["sourceDevice"],
        timestamp=envelope["timestamp"],
        dataMessage=map_dataMessage(envelope["dataMessage"]),
    )


class Role(Enum):
    system = 1
    user = 2
    assistant = 3


@dataclasses.dataclass
class ConversationMessage:
    role: Role
    message: str


@dataclasses.dataclass
class Conversation:
    def __init__(
        self,
        history: list[ConversationMessage] = [
            ConversationMessage(
                role=Role.system,
                message=MAIN_ADMIN_PROMPT,
            )
        ],
    ) -> None:
        self.history = history

    def add_message(self, message: ConversationMessage) -> None:
        self.history.append(message)

    def reset(self) -> None:
        self.history = [
            ConversationMessage(
                role=Role.system,
                message=MAIN_ADMIN_PROMPT,
            )
        ]

    def all_messages(self) -> list[ConversationMessage]:
        return self.history

    def get_conversation_in_chat_format(self) -> list[dict[str, str]]:
        return [
            {"role": x.role.name, "content": x.message} for x in self.all_messages()
        ]

    def get_last_message(self) -> ConversationMessage:
        return self.history[-1]
