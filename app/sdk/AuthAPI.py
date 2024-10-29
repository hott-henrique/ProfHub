import os

import requests

from model.Login import Login
from model.Register import Register


class AuthAPI:

    @classmethod
    def register(cls, register: Register) -> str:
        data = register.model_dump()

        data["birthdate"] = data["birthdate"].isoformat()

        response = requests.post(
            url=os.environ.get("API_URL", "http://localhost:8080/api/register"),
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")
            if response.status_code == 409:
                raise Exception("Já existe um usuário cadastrado com este email.")

        return response.json()


    @classmethod
    def login(cls, login: Login) -> str:
        response = requests.post(
            url=os.environ.get("API_URL", "http://localhost:8080/api/login"),
            json=login.model_dump()
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")
            if response.status_code == 401:
                raise Exception("Senha incorreta.")
            if response.status_code == 404:
                raise Exception("Não foi possível encontrar este usuário.")

        return response.json()
