from api.persistence.CentralPersistence import CentralPersistence

from api.control.AuthController import AuthController
from api.control.UserController import UserController


class CentralController(object):

    def __init__(self):
        self.persistence = CentralPersistence()
        self.auth = AuthController(persistence=self.persistence)
        self.user = UserController(persistence=self.persistence)

    def commit(self):
        self.persistence.commit()

    def rollback(self):
        self.persistence.commit()
