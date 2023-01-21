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


class EventsList(BaseModel):
    list: list[ShortEvent]


class FullEvent(ShortEvent):
    request_content_type: str

    class Config:
        extra = Extra.allow


class FullEventCache(BaseModel):
    __root__: dict[UUID, FullEvent]


class IndexCache(BaseModel):
    __root__: dict[UUID, int]
