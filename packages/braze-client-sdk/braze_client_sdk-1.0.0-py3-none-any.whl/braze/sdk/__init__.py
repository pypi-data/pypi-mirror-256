__all__ = [
    "Braze"
]

import functools

from .endpoint import (
    ContentBlocks,
    Users
)


class Braze:

    def __init__(
            self,
            host: str,
            token: str
    ):
        self.token = token
        self.host = host

    @functools.cached_property
    def content_blocks(self) -> ContentBlocks:
        return ContentBlocks(self)

    @functools.cached_property
    def users(self) -> Users:
        return Users(self)
