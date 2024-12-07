from api.persistence.CentralPersistence import CentralPersistence

from model.LanguageKnowledge import LanguageKnowledge, LanguageProciencyLevel


class LanguageKnowledgeController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, language_knowledge: LanguageKnowledge) -> int | None:
        return self.persistence.language_knowledge.create(language_knowledge=language_knowledge.model_dump())

    def update(self, id: int, language_knowledge: LanguageKnowledge) -> bool:
        return self.persistence.language_knowledge.update(id=id, language_knowledge=language_knowledge.model_dump())

    def delete(self, id: int) -> bool:
        return self.persistence.language_knowledge.delete(id=id)

    def get_all_from_uid(self, uid: int) -> list[LanguageKnowledge]:
        return [ LanguageKnowledge.validate(a) for a in self.persistence.language_knowledge.get_all_from_uid(uid=uid) ]

    def search_by_text(self, query: str, proficiency_level: LanguageProciencyLevel | None) -> list[LanguageKnowledge]:
        return [
            LanguageKnowledge.validate(a)
            for a
            in self.persistence.language_knowledge.search(
                query=query,
                proficiency_level=proficiency_level.value if proficiency_level else None
            )
        ]
