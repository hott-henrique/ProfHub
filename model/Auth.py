import pydantic


class Auth(pydantic.BaseModel):
    uid: int
    password_hash: str
