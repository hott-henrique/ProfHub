import os

import requests

from model.Course import Course


class CourseAPI:

    @classmethod
    def create(cls, course: Course) -> int:
        data = course.model_dump()

        data["date"] = data["date"].isoformat()

        response = requests.post(
            url=os.environ['API_URL'] + "/api/course/",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def update(cls, id: int, course: Course) -> bool:
        data = course.model_dump()

        data["date"] = data["date"].isoformat()

        response = requests.put(
            url=os.environ['API_URL'] + f"/api/course/{id}",
            json=data
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def delete(cls, id: int) -> bool:
        response = requests.delete(
            url=os.environ['API_URL'] +f"/api/course/{id}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def get_all_from_uid(cls, uid: int) -> list[Course]:
        response = requests.get(
            url=os.environ['API_URL'] + f"/api/course/{uid}",
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()

    @classmethod
    def search_by_text(cls, query: str) -> list[Course]:
        response = requests.get(
            url=os.environ['API_URL'] +"/api/course/search/",
            params=dict(query=query)
        )

        if not response.ok:
            if response.status_code >= 500:
                raise Exception("Algo de errado no servidor, por favor, contate o suporte.")

        return response.json()
