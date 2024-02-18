__all__ = [
    "prepare_request"
]

import functools
from typing import Optional

import requests


def prepare_request(
        method: Optional[str] = "GET",
        **kwargs
):
    return functools.partial(
        requests.request,
        method=method,
        **kwargs
    )
