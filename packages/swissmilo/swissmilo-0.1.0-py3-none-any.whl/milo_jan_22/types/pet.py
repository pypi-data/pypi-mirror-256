# File generated from our OpenAPI spec by Stainless.

from typing import Optional

from .._models import BaseModel

__all__ = ["Pet"]


class Pet(BaseModel):
    id: int

    name: str

    tag: Optional[str] = None
