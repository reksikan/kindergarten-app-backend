from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base

if TYPE_CHECKING:
    from .staff import Staff


class Job(IDMixin, Base):
    __tablename__ = 'jobs'

    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str | None] = mapped_column(String, nullable=True)

    staff: Mapped[List['Staff']] = relationship('Staff', uselist=True, lazy='selectin', back_populates='job')

    def __str__(self):
        return self.name
