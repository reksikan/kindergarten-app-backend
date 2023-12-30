from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base

if TYPE_CHECKING:
    from .address import Address


class City(IDMixin, Base):
    __tablename__ = 'cities'

    name: Mapped[str] = mapped_column(String, nullable=False)

    addresses: Mapped[List['Address']] = relationship('Address', uselist=True, lazy='selectin', back_populates='city')

    def __str__(self):
        return self.name
