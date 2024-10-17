import typing as t
import datetime as dt

import pydantic


class Language(pydantic.BaseModel):
    id: t.Optional[int] = None
    name: str = pydantic.Field(max_length=128)
