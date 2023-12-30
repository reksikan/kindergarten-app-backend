from datetime import date
from typing import TYPE_CHECKING

from fastapi_storages import StorageFile
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import String, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin
from .phone import Phone
from src.enums.gender import Gender
from src.common.storage import storage

if TYPE_CHECKING:
    from .address import Address
    from .child import Child
    from .staff import Staff
    from .parent import Parent


class Profile(IDMixin, Base):
    __tablename__ = 'profiles'

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birthdate: Mapped[date] = mapped_column(String, nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(*[v.value for v in Gender], name='gender'), nullable=False)
    avatar: Mapped[StorageFile] = mapped_column(FileType(storage=storage), nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('phones.id'), nullable=True)

    phone: Mapped[Phone | None] = relationship(Phone, uselist=False, lazy='selectin')

    address: Mapped['Address'] = relationship('Address', uselist=False, lazy='selectin', back_populates='profile')
    child: Mapped['Child'] = relationship('Child', uselist=False, lazy='selectin', back_populates='profile')
    staff: Mapped['Staff'] = relationship('Staff', uselist=False, lazy='selectin', back_populates='profile')
    parent: Mapped['Parent'] = relationship('Parent', uselist=False, lazy='selectin', back_populates='profile')

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'
