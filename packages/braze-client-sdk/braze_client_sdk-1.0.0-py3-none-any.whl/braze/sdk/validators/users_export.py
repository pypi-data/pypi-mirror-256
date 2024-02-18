from __future__ import annotations  # for Python 3.7–3.9

from pydantic import Field
from typing_extensions import (
    Annotated,
    Dict,
    List,
    NotRequired,
    TypedDict, Literal
)

__all__ = [
    "UsersExportGlobalControlGroupBody",
    "UsersExportIdsBody",
    "UsersExportSegmentBody"
]


class UsersExportGlobalControlGroupBody(TypedDict):
    callback_endpoint: NotRequired[str]
    fields_to_export: Annotated[List[str], Field(min_length=1)]
    output_format: NotRequired[Literal["gzip", "zip"]]


class UsersExportIdsBody(TypedDict):
    external_ids: NotRequired[List[str]]
    user_aliases: NotRequired[List[Dict]]
    device_id: NotRequired[str]
    braze_id: NotRequired[str]
    email_address: NotRequired[str]
    phone: NotRequired[str]
    fields_to_export: NotRequired[List[str]]


class UsersExportSegmentBody(TypedDict):
    segment_id: str
    callback_endpoint: NotRequired[str]
    fields_to_export: Annotated[List[str], Field(min_length=1)]
    output_format: NotRequired[Literal["gzip", "zip"]]
