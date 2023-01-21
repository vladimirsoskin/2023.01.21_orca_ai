import json
from typing import Optional

from pydantic.json import UUID

from events.messages import ShortEvent, FullEvent, FullEventCache, IndexCache, Direction

cache_list: list[ShortEvent]
cache_index: IndexCache
cache_full: FullEventCache


def init_cache():
    with open("events/events_sample.json") as file:
        global cache_list
        all_events = json.load(file)
        cache_list = [ShortEvent(**event) for event in all_events]
        cache_list = sorted(cache_list, key=lambda event: event.timestamp)

        global cache_index
        cache_index = {event.id: ind for ind, event in enumerate(cache_list)}

        global cache_full
        cache_full = {UUID(event["id"]): FullEvent(**event) for event in all_events}


def get_events_list(
        limit: int,
        direction: Direction,
        from_uuid: Optional[UUID] = None
) -> tuple[list[ShortEvent], int, int]:
    from_ind = 0
    if from_uuid is not None:
        base_ind = cache_index[from_uuid]
        from_ind = base_ind + 1 if direction == Direction.next else base_ind - 1
    to_ind = from_ind + limit if direction == Direction.next else from_ind - limit
    start_ind = max(0, min(from_ind, to_ind))
    end_ind = max(from_ind, to_ind)
    events_list = cache_list[start_ind: end_ind]
    events_amount = len(cache_list)
    events_left = events_amount - end_ind if direction == Direction.next else start_ind
    return events_list, events_amount, events_left


def get_event(uuid: UUID) -> Optional[FullEvent]:
    if uuid in cache_full:
        return cache_full[uuid]
    return None
