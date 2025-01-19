from typing import Any

from metagpt.schema import Message


class MessageWithLabel(Message):
    label: str = None  # A label to mark this message's type,function,etc.

    def __init__(self, label: str = "", content: str = "", **data: Any):
        data["content"] = data.get("content", content)
        data["label"] = data.get("label", label)
        super().__init__(**data)
