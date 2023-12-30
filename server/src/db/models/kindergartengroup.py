from typing import TYPE_CHECKING, List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base
from .kindergarten import Kindergarten

if TYPE_CHECKING:
    from .kindergartengroupstaff import KindergartenGroupStaff
    from .child import Child


class KindergartenGroup(IDMixin, Base):
    __tablename__ = 'kindergarten_groups'

    kindergarten_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergartens.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age_min: Mapped[int] = mapped_column(Integer, nullable=False)
    age_max: Mapped[int] = mapped_column(Integer, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    kindergarten: Mapped[Kindergarten] = relationship(Kindergarten, uselist=False, lazy='selectin')

    children: Mapped[List['Child']] = relationship(
        'Child', uselist=True, lazy='selectin', back_populates='group', foreign_keys='Child.group_id'
    )
    current_children: Mapped[List['Child']] = relationship(
        'Child', uselist=True, lazy='selectin', back_populates='current_group', foreign_keys='Child.current_group_id'
    )
    kindergarten_group_staff: Mapped[List['KindergartenGroupStaff']] = relationship(
        'KindergartenGroupStaff', uselist=True, lazy='selectin', back_populates='kindergarten_group'
    )

    def __str__(self):
        return self.name
