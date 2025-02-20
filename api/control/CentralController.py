from api.persistence.CentralPersistence import CentralPersistence

from api.control.AuthController import AuthController
from api.control.UserController import UserController
from api.control.AcademicBackgroundController import AcademicBackgroundController
from api.control.WorkingExperienceController import WorkingExperienceController
from api.control.CourseController import CourseController
from api.control.CertificateController import CertificateController
from api.control.LanguageKnowledgeController import LanguageKnowledgeController


class CentralController(object):

    def __init__(self):
        self.persistence = CentralPersistence()
        self.auth = AuthController(persistence=self.persistence)
        self.user = UserController(persistence=self.persistence)
        self.academic_background = AcademicBackgroundController(persistence=self.persistence)
        self.working_experience = WorkingExperienceController(persistence=self.persistence)
        self.course = CourseController(persistence=self.persistence)
        self.certificate = CertificateController(persistence=self.persistence)
        self.language_knowledge = LanguageKnowledgeController(persistence=self.persistence)

    def commit(self):
        self.persistence.commit()

    def rollback(self):
        self.persistence.commit()
