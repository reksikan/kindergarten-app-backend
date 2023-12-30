from .sbp.mock import SBPMock
from .sms.mock import MockSMSService
from .email.smtp import SMTPEmailService
from .dock_generator.dock_generator import DockGenerator


class ServiceManager:

    def __init__(self):
        self._sbp_client = SBPMock()
        self._sms_client = MockSMSService()
        self._email_client = SMTPEmailService()
        self._dock_generator = DockGenerator()

    @property
    def sbp_client(self):
        return self._sbp_client

    @property
    def email_client(self):
        return self._email_client

    @property
    def sms_client(self):
        return self._sms_client

    @property
    def dock_generator(self):
        return self._dock_generator
