from datetime import datetime

from sqlalchemy import DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .account import Account
from .phone import Phone
from .base import IDMixin, CreatedAtMixin, Base


class PhonedRecoveryRequest(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'phone_recovery_requests'

    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=False)
    phone_id: Mapped[int] = mapped_column(Integer, ForeignKey('phones.id'), nullable=False)

    account: Mapped[Account] = relationship(Account, uselist=False, lazy='select')
    phone: Mapped[Phone] = relationship(Phone, uselist=False, lazy='selectin')

    def __str__(self):
        return self.phone
