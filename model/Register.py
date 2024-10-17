import datetime as dt

import pydantic


class Register(pydantic.BaseModel):
    email: str = pydantic.Field(max_length=254)
    password: str
    name: str = pydantic.Field(max_length=128)
    phone: str = pydantic.Field(max_length=128)
    github: str = pydantic.Field(max_length=128)
    birthdate: dt.datetime
