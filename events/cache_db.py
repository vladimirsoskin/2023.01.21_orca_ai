import json
from typing import Optional

from pydantic.json import UUID

from events.messages import ShortEvent, FullEvent, FullEventCache, IndexCache, Direction, UsersIndex

cache_list: list[ShortEvent]
cache_index: IndexCache
cache_full: FullEventCache
cache_users: UsersIndex


def init_cache():
    with open("events/events_sample.json") as file:
        global cache_list
        all_events = json.load(file)
        cache_list = [ShortEvent(**event) for event in all_events]
        cache_list = sorted(cache_list, key=lambda event: event.timestamp)
        print("cache_list initialized")

        global cache_index
        cache_index = {event.id: ind for ind, event in enumerate(cache_list)}
        print("cache_index initialized")

        global cache_full
        cache_full = {UUID(event["id"]): FullEvent(**event) for event in all_events}
        print("cache_full initialized")

        global cache_users
        cache_users = {}
        for ind, event in enumerate(cache_list):
            user_ind = cache_users.get(event.user_id, list())
            user_ind.append(ind)
            cache_users[event.user_id] = user_ind
        print("cache_full initialized")


def _get_ind_values(
        from_ind: int,
        direction: Direction,
        limit: int,
        events_amount: int
) -> tuple[int, int, int]:
    to_ind = from_ind + limit if direction == Direction.next else from_ind - limit
    start_ind = max(0, min(from_ind, to_ind, events_amount))
    end_ind = min(events_amount, max(from_ind, to_ind))
    events_left = events_amount - end_ind if direction == Direction.next else start_ind
    return start_ind, end_ind, events_left


def get_events_list(
        limit: int,
        direction: Direction,
        from_uuid: Optional[UUID] = None
) -> tuple[list[ShortEvent], int, int]:
    from_ind = 0
    if from_uuid is not None:
        base_ind = cache_index[from_uuid]
        from_ind = base_ind + 1 if direction == Direction.next else base_ind - 1
    events_amount = len(cache_list)
    start_ind, end_ind, events_left = _get_ind_values(from_ind, direction, limit, events_amount)
    events_list = cache_list[start_ind: end_ind]

    return events_list, events_amount, events_left


def get_user_events(
        limit: int,
        direction: Direction,
        from_ind: int,
        user_uuid: UUID
) -> tuple[list[ShortEvent], int, int]:
    user_ind = cache_users.get(user_uuid)
    if user_ind is None:
        return [], 0, 0

    events_amount = len(user_ind)
    start_ind, end_ind, events_left = _get_ind_values(from_ind, direction, limit, events_amount)
    user_events_ind = user_ind[start_ind: end_ind]
    events_list = [cache_list[ind] for ind in user_events_ind]
    return events_list, events_amount, events_left


def get_event(uuid: UUID) -> Optional[FullEvent]:
    if uuid in cache_full:
        return cache_full[uuid]
    return None
