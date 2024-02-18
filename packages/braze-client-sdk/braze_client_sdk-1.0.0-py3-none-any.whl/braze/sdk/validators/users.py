from __future__ import annotations  # for Python 3.7–3.9

from pydantic import Field
from typing_extensions import (
    Annotated,
    Dict,
    Literal,
    List,
    NotRequired,
    TypedDict
)

__all__ = [
    "UsersDeleteBody",
    "UsersIdentifyBody",
    "UsersMergeBody",
    "UsersTrackBody"
]


class UsersDeleteBody(TypedDict):
    external_ids: NotRequired[List[str]]
    user_aliases: NotRequired[List[Dict]]
    braze_ids: NotRequired[List[str]]


class UsersIdentifyBody(TypedDict):
    aliases_to_identify: List[Dict]
    merge_behavior: NotRequired[Literal["merge", "none"]]


class UsersMergeBody(TypedDict):
    merge_updates: Annotated[List[Dict], Field(min_length=1)]


class UsersTrackBody(TypedDict):
    attributes: NotRequired[List[Dict]]
    events: NotRequired[List[Dict]]
    purchases: NotRequired[List[Dict]]
