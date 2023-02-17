import dataclasses
from uuid import UUID
from typing import List


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
    groupInfo: GroupInfo | None = None
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
