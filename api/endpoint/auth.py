import os
import uuid

import fastapi

import psycopg2
import psycopg2.extras
import pydantic

from api.control.connector import get_controller

from model.Register import Register
from model.Auth import Auth
from model.Login import Login
from model.User import User

import werkzeug.security


router = fastapi.APIRouter()

@router.post("/register")
def register(data: Register) -> str:
    controller = get_controller()

    user = User.model_validate({
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "birthdate": data.birthdate,
        "github": data.github
    })

    controller.user.create(user=user)

    if not user.id:
        controller.rollback()
        raise fastapi.exceptions.HTTPException(status_code=500, detail="Failed to create user.")

    auth = Auth.model_validate({
        "uid": user.id,
        "password_hash": werkzeug.security.generate_password_hash(data.password)
    })

    controller.auth.create(auth=auth)

    controller.commit()

    return "OK"

@router.post("/login")
def login(data: Login) -> str:
    controller = get_controller()
    return str(uuid.uuid4())
