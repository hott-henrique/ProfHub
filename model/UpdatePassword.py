import pydantic


class UpdatePassword(pydantic.BaseModel):
    email: str = pydantic.Field(max_length=254)
    old_password: str = pydantic.Field(max_length=128)
    new_password: str = pydantic.Field(max_length=128)
