from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base

if TYPE_CHECKING:
    from .address import Address


class Region(IDMixin, Base):
    __tablename__ = 'regions'

    name: Mapped[str] = mapped_column(String, nullable=False)

    addresses: Mapped[List['Address']] = relationship('Address', uselist=True, lazy='select', back_populates='region')

    def __str__(self):
        return f'{self.name}'