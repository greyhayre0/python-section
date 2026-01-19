import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class MessageParsed(ABC):
    """Абстракция для всех"""

    @abstractmethod
    def parse(self, payload: str) -> ParsedMessage:
        pass


class ParserFactory:
    """Фабрика"""

    def __init__(self):
        self._parsers: Dict[MessageType, MessageParsed] = {}

    def register(self, m_type: MessageType, parser: MessageParsed) -> None:
        self._parsers[m_type] = parser

    def create(self, m_type: MessageType) -> Optional[MessageParsed]:
        return self._parsers.get(m_type)

    def parse(self, json_m: JsonMessage):
        parser = self.create(json_m.message_type)
        if not parser:
            raise ValueError
        return parser.parse(json_m.payload)


class TelegramParser(MessageParsed):
    def parse(self, payload: str) -> ParsedMessage:
        print("Telegramm")
        return ParsedMessage()


class MattermostParser(MessageParsed):
    def parse(self, payload: str) -> ParsedMessage:
        print("Mattermost")
        return ParsedMessage()


class SlackParser(MessageParsed):
    def parse(self, payload: str) -> ParsedMessage:
        print("Slack")
        return ParsedMessage()
