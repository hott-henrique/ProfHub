import os

import requests

from model.WorkingExperience import WorkingExperience


class WorkingExperienceAPI:

    @classmethod
    def create(cls, working_experience: WorkingExperience) -> int:
        data = working_experience.model_dump()

        data["starting_date"] = data["starting_date"].isoformat()
        data["ending_date"] = data["ending_date"].isoformat()

        response = requests.post(
            url="http://localhost:8080/api/working-experience/",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def update(cls, id: int, working_experience: WorkingExperience) -> bool:
        data = working_experience.model_dump()

        data["starting_date"] = data["starting_date"].isoformat()
        data["ending_date"] = data["ending_date"].isoformat()

        response = requests.put(
            url=f"http://localhost:8080/api/working-experience/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=f"http://localhost:8080/api/working-experience/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def get_all_from_uid(cls, uid: int) -> list[WorkingExperience]:
        response = requests.get(
            url=f"http://localhost:8080/api/working-experience/{uid}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_text(cls, query: str) -> list[WorkingExperience]:
        response = requests.get(
            url=f"http://localhost:8080/api/working-experience/search/",
            params=dict(query=query)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
