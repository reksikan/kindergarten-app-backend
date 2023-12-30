from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, CreatedAtMixin, Base
from .kindergarten import Kindergarten
from .child import Child
from src.enums.receipt import ReceiptType, ReceiptStatus

if TYPE_CHECKING:
    from .sbp_payment import SBPPayment


class Receipt(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'receipts'

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    kindergarten_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergartens.id'), nullable=False)
    child_id: Mapped[int] = mapped_column(Integer, ForeignKey('children.id'), nullable=False)
    type: Mapped[ReceiptType] = mapped_column(
        Enum(*[v.value for v in ReceiptType], name='receipt_type'), nullable=False
    )
    status: Mapped[ReceiptStatus] = mapped_column(
        Enum(*[v.value for v in ReceiptStatus], name='receipt_status'), nullable=False
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    kindergarten: Mapped[Kindergarten] = relationship(Kindergarten, uselist=False, lazy='selectin')
    child: Mapped[Child] = relationship(Child, uselist=False, lazy='selectin')
    sbp_payment: Mapped[Optional['SBPPayment']] = relationship(
        'SBPPayment', uselist=False, lazy='selectin', back_populates='receipt'
    )

    def __str__(self):
        return f'{self.amount} at {self.created_at}'
