from api.persistence.CentralPersistence import CentralPersistence

from model.Course import Course


class CourseController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, course: Course) -> int | None:
        return self.persistence.course.create(course=course.model_dump())

    def update(self, id: int, course: Course) -> bool:
        return self.persistence.course.update(id=id, course=course.model_dump())

    def delete(self, id: int) -> bool:
        return self.persistence.course.delete(id=id)

    def get_all_from_uid(self, uid: int) -> list[Course]:
        return [ Course.validate(a) for a in self.persistence.course.get_all_from_uid(uid=uid) ]

    def search_by_text(self, query: str) -> list[Course]:
        return [
            Course.validate(a)
            for a
            in self.persistence.course.search(query=query)
        ]
