from datetime import datetime

from sqlalchemy import DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, CreatedAtMixin, Base
from .account import Account


class PasswordRecoveryRequest(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'password_recovery_requests'

    expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=False)

    account: Mapped[Account] = relationship(Account, uselist=False, lazy='selectin')

    def __str__(self):
        return f'{self.account_id}: {self.code}'
