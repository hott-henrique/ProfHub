import typing as t
import datetime as dt

import pydantic


class User(pydantic.BaseModel):
    id: t.Optional[int] = None
    name: str = pydantic.Field(max_length=128)
    email: str = pydantic.Field(max_length=254)
    phone: str = pydantic.Field(max_length=128)
    github: str = pydantic.Field(max_length=128)
    birthdate: dt.datetime
