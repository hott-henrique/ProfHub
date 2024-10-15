import typing as t
import datetime as dt

import pydantic


class Certificate(pydantic.BaseModel):
    id: int = 0
    uid: int
    name: str = pydantic.Field(max_length=32)
    validation_key: str
    date: dt.datetime
    expire_date: dt.datetime
