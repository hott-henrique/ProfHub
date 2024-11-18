import fastapi

import psycopg2

import pydantic

import werkzeug.security

from api.control.connector import get_controller

from model.Register import Register
from model.Auth import Auth
from model.Login import Login
from model.User import User


router = fastapi.APIRouter(prefix="/auth")

@router.post("/register")
def register(data: Register) -> User:
    controller = get_controller()

    user = User.model_validate({
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "birthdate": data.birthdate,
        "github": data.github
    })

    try:
        controller.user.create(user=user)
    except psycopg2.errors.UniqueViolation:
        controller.rollback()
        raise fastapi.exceptions.HTTPException(status_code=409, detail="Email already in use.")

    if not user.id:
        controller.rollback()
        raise fastapi.exceptions.HTTPException(status_code=500, detail="Server error.")

    auth = Auth.model_validate({
        "uid": user.id,
        "password_hash": werkzeug.security.generate_password_hash(data.password)
    })

    controller.auth.create(auth=auth)

    controller.commit()

    return controller.user.get_user_by_id(id=auth.uid)

@router.post("/login")
def login(data: Login) -> User:
    controller = get_controller()

    try:
        user = controller.user.get_user_by_email(email=data.email)
    except pydantic.ValidationError:
        raise fastapi.exceptions.HTTPException(status_code=404, detail="Email not registered yet.")

    auth = controller.auth.get_user_auth_info(user)

    if werkzeug.security.check_password_hash(auth.password_hash, data.password):
        return controller.user.get_user_by_id(id=auth.uid)

    raise fastapi.exceptions.HTTPException(status_code=401, detail="Wrong password")
