from api.persistence.CentralPersistence import CentralPersistence

from model.Auth import Auth
from model.User import User


class AuthController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, auth: Auth):
        self.persistence.auth.create(auth=auth.model_dump())

    def get_user_auth_info(self, user: User) -> Auth:
        if user.id is None or user.id == 0:
            raise Exception("AuthController received an invalid user.")

        auth_data = self.persistence.auth.get_auth_info_by_uid(uid=user.id)

        return Auth.model_validate(auth_data)
