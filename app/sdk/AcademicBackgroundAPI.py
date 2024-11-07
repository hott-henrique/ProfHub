import os

import requests

from model.AcademicBackground import AcademicBackground, EducationLevel


class AcademicBackgroundAPI:

    @classmethod
    def create(cls, academic_background: AcademicBackground) -> int:
        data = academic_background.model_dump()

        data["starting_date"] = data["starting_date"].isoformat()
        data["ending_date"] = data["ending_date"].isoformat()

        response = requests.post(
            url="http://localhost:8080/api/academic-background/",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def update(cls, id: int, academic_background: AcademicBackground) -> bool:
        data = academic_background.model_dump()

        data["starting_date"] = data["starting_date"].isoformat()
        data["ending_date"] = data["ending_date"].isoformat()

        response = requests.put(
            url=f"http://localhost:8080/api/academic-background/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=f"http://localhost:8080/api/academic-background/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def get_all_from_uid(cls, uid: int) -> list[AcademicBackground]:
        response = requests.get(
            url=f"http://localhost:8080/api/academic-background/{uid}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    # TODO: add EducationLevel argument.
    @classmethod
    def search_by_text(cls, query: str, education_level: EducationLevel) -> list[AcademicBackground]:
        response = requests.get(
            url=f"http://localhost:8080/api/academic-background/search/",
            params=dict(query=query, education_level=education_level)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
