from typing import Optional

from fastapi import APIRouter, status
from pydantic.types import UUID

from events.cache_db import get_events_list, get_event, get_user_events
from events.messages import EventsList, FullEvent, Direction

DEFAULT_PAGE_SIZE = 50

router = APIRouter(prefix="/events")


@router.get("/", response_model=EventsList)
async def get_list(
        anchor: Optional[UUID] = None,
        limit: Optional[int] = DEFAULT_PAGE_SIZE,
        direction: Optional[Direction] = Direction.next
):
    events_list, events_amount, events_left = get_events_list(limit, direction, anchor)
    return {"list": events_list, "amount": events_amount, "left": events_left}


@router.get("/user/{uuid}", response_model=EventsList)
async def get_list(
        uuid: UUID,
        from_ind: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_PAGE_SIZE,
        direction: Optional[Direction] = Direction.next,
):
    events_list, events_amount, events_left = get_user_events(limit, direction, from_ind, uuid)
    return {"list": events_list, "amount": events_amount, "left": events_left}


@router.get("/{uuid}", response_model=FullEvent)
async def get_entry(uuid: UUID):
    event = get_event(uuid)
    if event is None:
        return status.HTTP_404_NOT_FOUND
    return event
