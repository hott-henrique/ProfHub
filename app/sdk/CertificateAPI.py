import os

import requests

from model.Certificate import Certificate


class CertificateAPI:

    @classmethod
    def create(cls, certificate: Certificate) -> int:
        data = certificate.model_dump()

        data["date"] = data["date"].isoformat()
        data["expire_date"] = data["expire_date"].isoformat()

        response = requests.post(
            url=os.environ['API_URL'] + "/certificate/",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def update(cls, id: int, certificate: Certificate) -> bool:
        data = certificate.model_dump()

        data["date"] = data["date"].isoformat()
        data["expire_date"] = data["expire_date"].isoformat()

        response = requests.put(
            url=os.environ['API_URL'] + f"/certificate/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=os.environ['API_URL'] +f"/certificate/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def get_all_from_uid(cls, uid: int) -> list[Certificate]:
        response = requests.get(
            url=os.environ['API_URL'] +f"/certificate/{uid}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_text(cls, query: str) -> list[Certificate]:
        response = requests.get(
            url=os.environ['API_URL'] +"/certificate/search/",
            params=dict(query=query)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
