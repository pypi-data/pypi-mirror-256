from __future__ import annotations

from typing import (
    Optional,
    TYPE_CHECKING
)

if TYPE_CHECKING:  # pragma: no cover
    from ..endpoint import Endpoint

__all__ = [
    "api"
]

import functools
from json import loads
from requests import Response

from .auth import BearerAuth
from shared.types import AnyCallableT


class Api:

    def inject_call(
            self,
            function: Optional[AnyCallableT] = None,
            endpoint: str = None
    ):
        if function is None:
            return functools.partial(
                self.inject_call,
                endpoint=endpoint
            )

        @functools.wraps(function)
        def impl(this: Endpoint, *args, **kwargs) -> dict:
            try:
                callable_request: functools.partial = function(this, *args, **kwargs)
                res: Response = callable_request(auth=BearerAuth(this.braze.token),
                                                 url=F"{this.braze.host}{endpoint}")

                res.raise_for_status()
                braze_response = loads(res.content)

                return braze_response
            except Exception:
                raise

        return impl


api = Api()
