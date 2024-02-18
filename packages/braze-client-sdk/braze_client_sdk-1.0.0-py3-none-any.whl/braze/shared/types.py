__all__ = [
    "AnyCallableT",
    "DictT"
]

from typing import (
    Any,
    Callable,
    TypeVar
)

AnyCallableT = TypeVar("AnyCallableT", bound=Callable[..., Any])
DictT = TypeVar("DictT", bound=dict)
