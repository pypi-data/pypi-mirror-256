from __future__ import annotations  # for Python 3.7–3.9

from annotated_types import Gt, Lt
from typing_extensions import (
    Annotated,
    Literal,
    List,
    NotRequired,
    TypedDict
)

__all__ = [
    "ContentBlocksCreateBody",
    "ContentBlocksUpdateBody",
    "ContentBlocksInfoParams",
    "ContentBlocksListParams"
]


class ContentBlocksCreateBody(TypedDict):
    name: Annotated[str, Lt(100)]
    description: NotRequired[Annotated[str, Lt(250)]]
    content: str
    state: NotRequired[Literal["active", "draft"]]
    tags: NotRequired[List[str]]


class ContentBlocksUpdateBody(TypedDict):
    content_block_id: str
    name: NotRequired[Annotated[str, Lt(100)]]
    description: NotRequired[Annotated[str, Lt(250)]]
    content: NotRequired[str]
    state: NotRequired[Literal["active", "draft"]]
    tags: NotRequired[List[str]]


class ContentBlocksInfoParams(TypedDict):
    content_block_id: str
    include_inclusion_data: NotRequired[bool]


class ContentBlocksListParams(TypedDict):
    modified_after: NotRequired[str]
    modified_before: NotRequired[str]
    limit: NotRequired[Annotated[int, Gt(0)]]
    offset: NotRequired[Annotated[int, Gt(0)]]
