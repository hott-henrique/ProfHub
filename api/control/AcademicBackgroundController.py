from api.persistence.CentralPersistence import CentralPersistence

from model.AcademicBackground import AcademicBackground, EducationLevel


class AcademicBackgroundController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, academic_background: AcademicBackground) -> int | None:
        return self.persistence.academic_background.create(academic_background=academic_background.model_dump())

    def update(self, id: int, academic_background: AcademicBackground) -> bool:
        return self.persistence.academic_background.update(id=id, academic_background=academic_background.model_dump())

    def delete(self, id: int) -> bool:
        return self.persistence.academic_background.delete(id=id)

    def get_all_from_uid(self, uid: int) -> list[AcademicBackground]:
        return [ AcademicBackground.validate(a) for a in self.persistence.academic_background.get_all_from_uid(uid=uid) ]

    def search_by_text(self, query: str, education_level: EducationLevel | None = None) -> list[AcademicBackground]:
        return [
            AcademicBackground.validate(a)
            for a
            in self.persistence.academic_background.search(query=query, education_level=education_level)
        ]
