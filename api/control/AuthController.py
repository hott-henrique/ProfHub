from api.persistence.CentralPersistence import CentralPersistence
from model.Auth import Auth


class AuthController(object):

    def __init__(self, persistence: CentralPersistence):
        self.persistence = persistence

    def create(self, auth: Auth):
        self.persistence.auth.create(auth=auth.model_dump())
