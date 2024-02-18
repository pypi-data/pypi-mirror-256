import datetime

from pydantic import Field

from poaster.core.schemas import BaseSchema


class PostInputSchema(BaseSchema):
    """Post input from user."""

    title: str = Field(max_length=255)
    text: str


class PostWithUsernameSchema(BaseSchema):
    """Post input from user with the username added."""

    title: str = Field(max_length=255)
    text: str
    username: str


class PostSchema(BaseSchema):
    """Post fetched from the persistence layer."""

    id: int
    title: str
    text: str
    created_by: str
    created_at: datetime.datetime
