import os

import fastapi

import psycopg2
import psycopg2.extras

from api.control.connector import get_controller

from api.endpoint import auth
from api.endpoint import academic_background


api = fastapi.FastAPI(title="ProfHub - API",
                      root_path="/api",
                      version="0.1.0")

@api.exception_handler(Exception)
async def unhandled_exception_handler(request: fastapi.Request, exc: Exception):
    controller = get_controller()

    controller.rollback()

    return fastapi.responses.JSONResponse(
        status_code=500,
        content={ "message": f"Something unkown went wrong, please contact support." }
    )

@api.get("/ping")
def ping():
    return "OK"

api.include_router(auth.router)
api.include_router(academic_background.router)
