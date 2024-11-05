from api.persistence.CentralPersistence import CentralPersistence

from model.WorkingExperience import WorkingExperience


class WorkingExperienceController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, working_experience: WorkingExperience) -> int | None:
        return self.persistence.working_experience.create(working_experience=working_experience.model_dump())

    def update(self, id: int, working_experience: WorkingExperience) -> bool:
        return self.persistence.working_experience.update(id=id, working_experience=working_experience.model_dump())

    def delete(self, id: int) -> bool:
        return self.persistence.working_experience.delete(id=id)

    def get_all_from_uid(self, uid: int) -> list[WorkingExperience]:
        return [ WorkingExperience.validate(a) for a in self.persistence.working_experience.get_all_from_uid(uid=uid) ]

    def search_by_text(self, query: str) -> list[WorkingExperience]:
        return [
            WorkingExperience.validate(a)
            for a
            in self.persistence.working_experience.search(query=query)
        ]
