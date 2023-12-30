from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base

if TYPE_CHECKING:
    from .disease import Disease


class DiseaseGroup(IDMixin, Base):
    __tablename__ = 'diseases_groups'

    note: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    diseases: Mapped[List['Disease']] = relationship('Disease', lazy='selectin', uselist=True, back_populates='group')

    def __str__(self):
        return f'{self.name}: {self.note}'
