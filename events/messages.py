from enum import Enum

from pydantic import BaseModel, Extra
from pydantic.json import UUID
import datetime as dt


class Direction(Enum):
    next = "next"
    prev = "prev"


class ShortEvent(BaseModel):
    id: UUID
    timestamp: dt.datetime
    method: str
    call_path: str
    user_id: UUID


class EventsList(BaseModel):
    list: list[ShortEvent]
    amount: int
    left: int


class FullEvent(ShortEvent):
    request_content_type: str

    class Config:
        extra = Extra.allow


class FullEventCache(BaseModel):
    __root__: dict[UUID, FullEvent]


class IndexCache(BaseModel):
    __root__: dict[UUID, int]


class UsersIndex(BaseModel):
    __root__: dict[UUID, list[int]]
