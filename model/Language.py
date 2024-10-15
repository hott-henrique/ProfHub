import typing as t
import datetime as dt

import pydantic


class Language(pydantic.BaseModel):
    id: int = 0
    name: str = pydantic.Field(max_length=128)
