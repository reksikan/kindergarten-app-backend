class BaseSBPService:
    async def create_payment_link(self, amount: int) -> str:
        raise NotImplemented()

    async def check_payment_link(self, link: str) -> bool:
        raise NotImplemented()
