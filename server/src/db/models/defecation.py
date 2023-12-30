from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base

if TYPE_CHECKING:
    from .morningfilter import MorningFilter


class Defecation(IDMixin, Base):
    __tablename__ = 'defecations'

    value: Mapped[str] = mapped_column(String, nullable=False)

    morning_filters: Mapped[List['MorningFilter']] = relationship(
        'MorningFilter', uselist=False, lazy='selectin', back_populates='defecation'
    )

    def __str__(self):
        return self.value