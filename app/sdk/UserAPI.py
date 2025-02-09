import os

import requests

from model.User import User

class UserAPI:

    @classmethod
    def update(cls, id: int, user: User) -> bool:
        data = user.model_dump()

        data["birthdate"] = data["birthdate"].isoformat()

        response = requests.put(
            url=os.environ['API_URL'] + f"/user/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=os.environ['API_URL'] + f"/user/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_text(cls, query: str) -> list[User]:
        response = requests.get(
            url=os.environ['API_URL'] + "/user/search/",
            params=dict(query=query)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_id(cls, id: int) -> User:

        response = requests.get(
            url=os.environ['API_URL'] + f"/user/{id}",
        )

        if not response.ok:
            if response.status_code == 404:
                raise Exception(f"Usuário com ID {id} não encontrado.")
            elif response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def most_certified_professionals(cls, academic_background: str, page: int = 0, page_sz: int = 10) -> list[dict[str, int]]:
        response = requests.get(
            url=os.environ['API_URL'] + f"/user/most-certified/{academic_background}",
            params=dict(page=page, page_sz=page_sz)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def background_check(cls, term: str, page: int = 0, page_sz: int = 10) -> list[dict[str, int]]:
        response = requests.get(
            url=os.environ['API_URL'] + f"/user/background-check/{term}",
            params=dict(page=page, page_sz=page_sz)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
