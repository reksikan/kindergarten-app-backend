from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, IDMixin, CreatedAtMixin
from .account import Account


class Password(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'passwords'

    hash: Mapped[str] = mapped_column(String, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=False)
    is_temporary: Mapped[bool] = mapped_column(Boolean, default=False)

    account: Mapped[Account] = relationship(Account, uselist=False, lazy='selectin')

    def __str__(self):
        return f'password for account: {self.account_id}'


