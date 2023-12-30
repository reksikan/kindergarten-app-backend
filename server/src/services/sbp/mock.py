from .base import BaseSBPService


class SBPMock(BaseSBPService):
    link = 'https://google.com'
    is_paid = True

    async def create_payment_link(self, amount: int) -> str:
        return self.link

    async def check_payment_link(self, link: str) -> bool:
        return self.is_paid
