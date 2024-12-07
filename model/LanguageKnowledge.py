import enum

import typing as t

import pydantic


class Language(str, enum.Enum):
    GERMAN = "alemão"
    ARABIC = "árabe"
    EGYPTIAN_ARABIC = "árabe egípcio"
    BENGALI = "bengali"
    BURMESE = "birmanês"
    CHINESE = "chines"
    KOREAN = "coreano"
    KURDISH = "curdo"
    SPANISH = "espanhol"
    FRENCH = "francês"
    GUJARATI = "gujarati"
    HAUSA = "hausa"
    HINDI = "hindi"
    INDONESIAN = "indonésio"
    ENGLISH = "inglês"
    ITALIAN = "italiano"
    JAPANESE = "japonês"
    JAVANESE = "javanês"
    KANNADA = "kannada"
    MALAYALAM = "malaiala"
    MARATHI = "marathi"
    ODIA = "oriya"
    PERSIAN = "persa"
    POLISH = "polaco"
    PORTUGUESE = "português"
    PUNJABI = "punjabi"
    ROMANIAN = "romeno"
    RUSSIAN = "russo"
    SOMALI = "somali"
    SUNDANESE = "sundanês"
    TAGALOG = "tagalog"
    THAI = "tailandês"
    TAMIL = "tamil"
    TELUGU = "telugu"
    TURKISH = "turco"
    UKRAINIAN = "ucraniano"
    URDU = "urdu"
    VIETNAMESE = "vietnamita"

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
    language: Language
    proficiency_level: LanguageProciencyLevel = pydantic.Field(max_length=128)
