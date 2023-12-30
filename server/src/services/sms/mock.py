from .base import BaseSMSService
from httpx import AsyncClient

from settings import SMS_SERVICE_URL


class MockSMSService(BaseSMSService):
    async def send_sms(self, phone_number: str, text: str):
        async with AsyncClient(base_url=SMS_SERVICE_URL) as client:
            await client.post(url='/send', json={'phone_number': phone_number, 'text': text})
