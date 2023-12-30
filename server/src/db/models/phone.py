from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base

if TYPE_CHECKING:
    from .kindergarten import Kindergarten
    from .account import Account
    from .phonechangerequest import PhonedRecoveryRequest
    from .profile import Profile


class Phone(IDMixin, Base):
    __tablename__ = 'phones'

    phone: Mapped[str] = mapped_column(String, nullable=False)

    account: Mapped['Account'] = relationship('Account', uselist=False, lazy='select', back_populates='phone')
    profile: Mapped['Profile'] = relationship('Profile', uselist=False, lazy='selectin', back_populates='phone')
    kindergarten: Mapped['Kindergarten'] = relationship(
        'Kindergarten', uselist=False, lazy='selectin', back_populates='phone'
    )
    phone_change_request: Mapped[List['PhonedRecoveryRequest']] = relationship(
        'PhonedRecoveryRequest', uselist=True, lazy='select', back_populates='phone'
    )

    def __str__(self):
        return self.phone
