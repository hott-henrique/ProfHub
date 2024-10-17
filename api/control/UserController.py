from api.persistence.CentralPersistence import CentralPersistence
from model.User import User


class UserController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, user: User):
        user.id = self.persistence.user.create(user=user.model_dump())

    def get_user_by_email(self, email: str) -> User:
        user_data = self.persistence.user.get_by_email(email=email)
        return User.model_validate(user_data)
