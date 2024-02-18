__all__ = [
    "BearerAuth"
]

from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
