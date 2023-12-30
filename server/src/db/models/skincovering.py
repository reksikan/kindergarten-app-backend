from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, CreatedAtMixin

if TYPE_CHECKING:
    from .morningfilter import MorningFilter


class SkinCovering(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'skin_coverings'

    value: Mapped[str] = mapped_column(String, nullable=False)

    morning_filters: Mapped[List['MorningFilter']] = relationship(
        'MorningFilter', uselist=True, lazy='selectin', back_populates='skin_covering'
    )

    def __str__(self):
        return f'{self.value}'
