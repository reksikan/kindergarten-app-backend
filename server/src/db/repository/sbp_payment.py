from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from src.db.models.receipt import Receipt
from src.db.models.sbp_payment import SBPPayment
from src.db.repository.base import BaseRepository


class SBPPaymentRepository(BaseRepository):
    async def get_by_receipt_id(self, receipt_id) -> SBPPayment | None:
        async with self._client.session() as session:
            return (
                await session.scalars(
                    select(SBPPayment)
                    .join(SBPPayment.receipt)
                    .where(Receipt.id == receipt_id)
                )
            ).one_or_none()

    async def create_payment(self, receipt_id: int, link: str) -> SBPPayment:
        async with self._client.session() as session:
            payment = SBPPayment(
                receipt_id=receipt_id,
                link=link,
            )
            session.add(payment)
            await session.commit()
        return payment

