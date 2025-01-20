from enum import Enum

from pydantic import BaseModel


class TaskTypeDef(BaseModel):
    name: str
    desc: str = ""
    guidance: str = ""


class TaskType(Enum):
    """By identifying specific types of tasks, we can inject human priors (guidance) to help task solving"""

    OTHER = TaskTypeDef(name="other", desc="Any tasks not in the defined categories")

    # Legacy TaskType to support tool recommendation using type match. You don't need to define task types if you have no human priors to inject.
    TEXT2IMAGE = TaskTypeDef(
        name="text2image",
        desc="Related to text2image, image2image using stable diffusion model.",
    )
    WEBSCRAPING = TaskTypeDef(
        name="web scraping",
        desc="For scraping data from web pages.",
    )
    EMAIL_LOGIN = TaskTypeDef(
        name="email login",
        desc="For logging to an email.",
    )

    @property
    def type_name(self):
        return self.value.name

    @classmethod
    def get_type(cls, type_name):
        for member in cls:
            if member.type_name == type_name:
                return member.value
        return None
