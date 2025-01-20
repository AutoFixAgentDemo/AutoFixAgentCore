"""
An enhanced Memory class to add retrieve by label feature.
"""
from collections import defaultdict
from typing import DefaultDict

from metagpt.memory import Memory
from metagpt.schema import Message
from pydantic import Field, SerializeAsAny
from schema import MessageWithLabel

class MemoryWithLabel(Memory):
    index: DefaultDict[str, list[SerializeAsAny[MessageWithLabel]]] = Field(default_factory=lambda: defaultdict(list))

    def get_by_label(self, label: str) -> list[MessageWithLabel]:
        """Return all messages with a specified label"""
        return [message for message in self.storage if message.label == label]
