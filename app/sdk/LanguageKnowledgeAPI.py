import os

import requests

from model.LanguageKnowledge import LanguageKnowledge, LanguageProciencyLevel


class LanguageKnowledgeAPI:

    @classmethod
    def create(cls, language_knowledge: LanguageKnowledge) -> int:
        data = language_knowledge.model_dump()

        data["date"] = data["date"].isoformat()

        response = requests.post(
            url=os.environ['API_URL'] + "/api/language_knowledge/",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def update(cls, id: int, language_knowledge: LanguageKnowledge) -> bool:
        data = language_knowledge.model_dump()

        data["date"] = data["date"].isoformat()

        response = requests.put(
            url=os.environ['API_URL'] + f"/api/language_knowledge/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=os.environ['API_URL'] +f"/api/language_knowledge/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def get_all_from_uid(cls, uid: int) -> list[LanguageKnowledge]:
        response = requests.get(
            url=os.environ['API_URL'] +f"/api/language_knowledge/{uid}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_text(cls, query: str, proficiency_level: LanguageProciencyLevel | None) -> list[LanguageKnowledge]:
        response = requests.get(
            url=os.environ['API_URL'] +"/api/language_knowledge/search/",
            params=dict(query=query, proficiency_level=proficiency_level.value if proficiency_level else None)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
