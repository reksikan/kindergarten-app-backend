from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base
from .address import Address
from .phone import Phone

if TYPE_CHECKING:
    from .kindergartengroup import KindergartenGroup
    from .receipt import Receipt
    from .role import Role
    from .staff import Staff


class Kindergarten(IDMixin, Base):
    __tablename__ = 'kindergartens'

    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_id: Mapped[int] = mapped_column(Integer, ForeignKey('phones.id'), nullable=False, unique=True)

    address: Mapped[Address] = relationship(Address, uselist=False, lazy='selectin')
    phone: Mapped[Phone] = relationship(Phone, uselist=False, lazy='selectin')

    kindergartengroups: Mapped[List['KindergartenGroup']] = relationship(
        'KindergartenGroup', uselist=True, lazy='selectin', back_populates='kindergarten'
    )
    receipts: Mapped[List['Receipt']] = relationship(
        'Receipt', uselist=True, lazy='selectin', back_populates='kindergarten'
    )
    roles: Mapped[List['Role']] = relationship(
        'Role', uselist=True, lazy='selectin', back_populates='kindergarten'
    )
    staff: Mapped[List['Staff']] = relationship(
        'Staff', uselist=True, lazy='selectin', back_populates='kindergarten'
    )

    def __str__(self):
        return self.name
