import typing as t
import datetime as dt

import pydantic


class WorkingExperience(pydantic.BaseModel):
    id: int = 0
    uid: int
    job: str = pydantic.Field(max_length=32)
    company: str = pydantic.Field(max_length=128)
    starting_date: dt.datetime
    ending_date: dt.datetime
    description: str
