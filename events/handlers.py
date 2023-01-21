from typing import Optional

from fastapi import APIRouter, status
from pydantic.types import UUID

from events.db import get_events_list, get_event
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
    # TODO implement filter by user
    return {"list": events_list, "amount": events_amount, "left": events_left}


@router.get("/{uuid}", response_model=FullEvent)
async def get_entry(uuid: UUID):
    event = get_event(uuid)
    if event is None:
        return status.HTTP_404_NOT_FOUND
    return event
