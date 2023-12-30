from typing import Sequence

from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload

from .base import BaseRepository
from src.db.models.receipt import Receipt
from src.db.models.child import Child
from src.db.models.childparent import ChildParent
from src.db.models.parent import Parent
from src.db.models.kindergarten import Kindergarten
from src.db.models.staff import Staff
from src.enums.receipt import ReceiptType, ReceiptStatus


class ReceiptRepository(BaseRepository):
    async def receipts_by_parent_id(self, account_id) -> Sequence[Receipt]:
        async with self._client.session() as session:
            return (
                await session.scalars(
                    select(Receipt)
                    .join(Receipt.child)
                    .join(Child.child_parent)
                    .join(ChildParent.parent)
                    .where(
                        Parent.account_id == account_id
                    )
                    .order_by(Receipt.created_at)
                )
            ).unique().all()

    async def receipts_by_staff_id(self, account_id) -> Sequence[Receipt]:
        async with self._client.session() as session:
            return (
                await session.scalars(
                    select(Receipt)
                    .join(Receipt.kindergarten)
                    .join(Kindergarten.staff)
                    .where(
                        Staff.account_id == account_id
                    )
                    .order_by(Receipt.created_at)
                )
            ).unique().all()

    async def get_receipt_by_id(self, id_: int) -> Receipt | None:
        async with self._client.session() as session:
            return (
                await session.scalars(
                    select(Receipt)
                    .where(Receipt.id == id_)
                )
            ).one_or_none()

    async def create_receipt(
        self,
        child: Child,
        kindergarten: Kindergarten,
        type_: ReceiptType,
        amount: int,
    ) -> Receipt:
        async with self._client.session() as session:
            receipt = Receipt(
                child=child,
                kindergarten=kindergarten,
                type=type_,
                amount=amount,
                status=ReceiptStatus.NOT_PAID,
            )
            session.add(receipt)
            await session.commit()
            return receipt

    async def confirm_receipt(self, receipt: Receipt) -> Receipt:
        async with self._client.session() as session:
            receipt.status = ReceiptStatus.PAID
            session.add(receipt)
            await session.commit()
        return receipt
