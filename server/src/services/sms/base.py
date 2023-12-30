class BaseSMSService:
    async def send_sms(self, phone_number: str, text: str):
        raise NotImplemented()