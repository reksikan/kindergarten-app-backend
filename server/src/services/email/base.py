class BaseEmailService:
    async def send(self, to: str, title: str, content: str):
        raise NotImplemented()
