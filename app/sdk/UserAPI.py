import os

import requests

from model.User import User


class UserAPI:

    @classmethod
    def update(cls, id: int, user: User) -> bool:
        data = user.model_dump()

        data["birthdate"] = data["birthdate"].isoformat()

        response = requests.put(
            url=f"http://localhost:8080/api/user/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=f"http://localhost:8080/api/user/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_text(cls, query: str) -> list[User]:
        response = requests.get(
            url=f"http://localhost:8080/api/user/search/",
            params=dict(query=query)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
