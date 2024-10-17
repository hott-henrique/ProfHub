import pydantic


class Login(pydantic.BaseModel):
    email: str = pydantic.Field(max_length=254)
    password: str = pydantic.Field(max_length=128)
