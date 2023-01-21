from typing import Optional

from fastapi import APIRouter, status
from pydantic.types import UUID

from events.db import get_events_list, get_event
from events.messages import EventsList, FullEvent, Direction

DEFAULT_PAGE_SIZE = 50

router = APIRouter(prefix="/events")


@router.get("/", response_model=EventsList)
async def get_list(
        from_uuid: Optional[UUID] = None,
        limit: Optional[int] = DEFAULT_PAGE_SIZE,
        direction: Optional[Direction] = Direction.next
):
    events_list = get_events_list(limit, direction, from_uuid)
    return {"list": events_list}


@router.get("/{uuid}", response_model=FullEvent)
async def get_entry(uuid: UUID):
    event = get_event(uuid)
    if event is None:
        return status.HTTP_404_NOT_FOUND
    return event
