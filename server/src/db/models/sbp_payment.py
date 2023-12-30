from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, CreatedAtMixin
from .receipt import Receipt


class SBPPayment(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'sbp_payments'

    receipt_id: Mapped[int] = mapped_column(Integer, ForeignKey('receipts.id'), unique=True, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)

    receipt: Mapped[Receipt] = relationship(Receipt, uselist=False, lazy='selectin')

    def __str__(self):
        return f'{self.link}'