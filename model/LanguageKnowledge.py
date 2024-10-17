import enum

import typing as t
import datetime as dt

import pydantic


class LanguageProciencyLevel(str, enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

class LanguageKnowledge(pydantic.BaseModel):
    id: t.Optional[int] = None
    uid: int
    lid: int
    proficiency_level: LanguageProciencyLevel = pydantic.Field(max_length=128)
