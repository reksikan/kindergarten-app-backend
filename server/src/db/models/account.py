from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreatedAtMixin, IDMixin
from .phone import Phone

if TYPE_CHECKING:
    from .parent import Parent
    from .staff import Staff
    from .password import Password
    from .passwordrecoveryrequest import PasswordRecoveryRequest
    from .phonechangerequest import PhonedRecoveryRequest


class Account(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'accounts'

    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=True)
    phone_id: Mapped[int] = mapped_column(Integer, ForeignKey('phones.id'), nullable=False)

    phone: Mapped[Phone] = relationship(Phone, uselist=False, lazy='selectin')
    created_by: Mapped['Account'] = relationship(
        'Account', uselist=False, lazy='select', remote_side='Account.id',
    )

    created_accounts: Mapped[List['Account']] = relationship(
        'Account', uselist=True, lazy='select', back_populates='created_by'
    )
    passwords: Mapped[List['Password']] = relationship('Password', uselist=True, lazy='selectin', back_populates='account')
    staff: Mapped['Staff'] = relationship('Staff', uselist=False, lazy='selectin', back_populates='account')
    parent: Mapped['Parent'] = relationship('Parent', uselist=False, lazy='selectin', back_populates='account')
    password_recovery_requests: Mapped[List['PasswordRecoveryRequest']] = relationship(
        'PasswordRecoveryRequest', uselist=True, lazy='select', back_populates='account'
    )
    phone_change_requests: Mapped[List['PhonedRecoveryRequest']] = relationship(
        'PhonedRecoveryRequest', uselist=True, lazy='select', back_populates='account'
    )

    def __str__(self):
        return str(self.phone)
