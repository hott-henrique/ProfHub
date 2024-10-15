import typing as t
import datetime as dt

import pydantic


class Course(pydantic.BaseModel):
    id: int = 0
    uid: int
    name: str = pydantic.Field(max_length=32)
    workload: int
    date: dt.datetime
    description: str
