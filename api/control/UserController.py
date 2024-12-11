from api.persistence.CentralPersistence import CentralPersistence
from model.User import User


class UserController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, user: User):
        user.id = self.persistence.user.create(user=user.model_dump())

    def update(self, id: int, user: User) -> User:
        user_data = self.persistence.user.update(id=id, user=user.model_dump())
        return User.model_validate(user_data)

    def delete(self, id: int) -> bool:
        return self.persistence.user.delete(id=id)

    def get_user_by_email(self, email: str) -> User | None:
        user_data = self.persistence.user.get_by_email(email=email)
        return User.model_validate(user_data) if user_data else None

    def get_user_by_id(self, id: int) -> User | None:
        user_data = self.persistence.user.get_by_id(id=id)
        return User.model_validate(user_data) if user_data else None

    def search_by_text(self, query: str) -> list[User]:
        return [
            User.validate(a)
            for a
            in self.persistence.user.search(query=query)
        ]

    def get_most_certified_professionals_by_academic_background(self, academic_background: str, page_sz: int, page: int) -> list[tuple[int, int]]:
        return self.persistence.user.get_most_certified_professionals_by_academic_background(
            academic_background=academic_background,
            page_sz=page_sz,
            page=page
        )
