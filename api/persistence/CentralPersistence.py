from api.persistence.AuthPersistence import AuthPersistence
from api.persistence.UserPersistence import UserPersistence
from api.persistence.AcademicBackgroundPersistence import AcademicBackgroundPersistence
from api.persistence.WorkingExperiencePersistence import WorkingExperiencePersistence
from api.persistence.CoursePersistence import CoursePersistence
from api.persistence.CertificatePersistence import CertificatePersistence

from api.persistence.connector import get_postgres_db


class CentralPersistence(object):

    def __init__(self):
        self.auth = AuthPersistence()
        self.user = UserPersistence()
        self.academic_background = AcademicBackgroundPersistence()
        self.working_experience = WorkingExperiencePersistence()
        self.course = CoursePersistence()
        self.certificate = CertificatePersistence()

    def commit(self):
        get_postgres_db().commit()

    def rollback(self):
        get_postgres_db().rollback()
