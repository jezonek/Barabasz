from src.barabasz.parsers import Message, Envelope, DataMessage, GroupInfo, Mention
from uuid import UUID


def test_if_message_is_not_group():
    test_msg = Message(
        envelope=Envelope(
            source="+4912345678901",
            sourceNumber="+4912345678901",
            sourceUuid=UUID("b1234567-89c0-1234-a5c6-78ab90e123ea"),
            sourceName="Test Sender",
            sourceDevice=1,
            timestamp=1676137913645,
            dataMessage=DataMessage(
                timestamp=1676137913645,
                message="Dupa 12345",
                expiresInSeconds=0,
                viewOnce=False,
                groupInfo=None,
                mentions=[],
            ),
        ),
        account="+4912345678901",
        subscription=0,
    )
    assert not test_msg.is_group()


def test_if_message_is_group():
    test_msg = Message(
        envelope=Envelope(
            source="+4912345678901",
            sourceNumber="+4912345678901",
            sourceUuid=UUID("b1234567-89c0-1234-a5c6-78ab90e123ea"),
            sourceName="Test Sender",
            sourceDevice=1,
            timestamp=1676137913645,
            dataMessage=DataMessage(
                timestamp=1676137913645,
                message="Dupa 12345",
                expiresInSeconds=0,
                viewOnce=False,
                groupInfo=GroupInfo(groupId=1, groupType="abc"),
                mentions=[],
            ),
        ),
        account="+4912345678901",
        subscription=0,
    )
    assert test_msg.is_group()


def test_if_message_is_mentioned():
    test_msg = Message(
        envelope=Envelope(
            source="+4912345678901",
            sourceNumber="+4912345678901",
            sourceUuid=UUID("b1234567-89c0-1234-a5c6-78ab90e123ea"),
            sourceName="Test Sender",
            sourceDevice=1,
            timestamp=1676137913645,
            dataMessage=DataMessage(
                timestamp=1676137913645,
                message="Dupa 12345",
                expiresInSeconds=0,
                viewOnce=False,
                groupInfo=None,
                mentions=[
                    Mention(
                        name="+49123456789012",
                        number="+49123456789012",
                        uuid=UUID("b1234567-89c0-1234-a5c6-78ab90e123ea"),
                        start=1676137913645,
                        length=0,
                    ),
                ],
            ),
        ),
        account="+4912345678901",
        subscription=0,
    )
    assert test_msg.is_mentioned()
