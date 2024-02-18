from __future__ import annotations  # for Python 3.7–3.9

from pydantic import Field
from typing_extensions import (
    Annotated,
    Dict,
    List,
    TypedDict
)

__all__ = [
    "UsersAliasNewBody",
    "UsersAliasUpdateBody"
]


class UsersAliasNewBody(TypedDict):
    user_aliases: Annotated[List[Dict], Field(min_length=1)]


class UsersAliasUpdateBody(TypedDict):
    alias_updates: Annotated[List[Dict], Field(min_length=1)]
