import typing as t
import datetime as dt

import pydantic


class AcademicBackground(pydantic.BaseModel):
    id: t.Optional[int] = None
    uid: int
    name: str = pydantic.Field(max_length=32)
    institution: str = pydantic.Field(max_length=128)
    starting_date: dt.datetime
    ending_date: dt.datetime
    workload: int
    description: str
