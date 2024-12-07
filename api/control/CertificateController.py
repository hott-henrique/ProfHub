from api.persistence.CentralPersistence import CentralPersistence

from model.Certificate import Certificate


class CertificateController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, certificate: Certificate) -> int | None:
        return self.persistence.certificate.create(certificate=certificate.model_dump())

    def update(self, id: int, certificate: Certificate) -> bool:
        return self.persistence.certificate.update(id=id, certificate=certificate.model_dump())

    def delete(self, id: int) -> bool:
        return self.persistence.certificate.delete(id=id)

    def get_all_from_uid(self, uid: int) -> list[Certificate]:
        return [ Certificate.validate(a) for a in self.persistence.certificate.get_all_from_uid(uid=uid) ]

    def search_by_text(self, query: str) -> list[Certificate]:
        return [
            Certificate.validate(a)
            for a
            in self.persistence.certificate.search(query=query)
        ]
