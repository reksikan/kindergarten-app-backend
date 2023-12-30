from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, IDMixin
from .profile import Profile
from .kindergartengroup import KindergartenGroup
from .medicinecard import MedicineCard

if TYPE_CHECKING:
    from .childparent import ChildParent
    from .morningfilter import MorningFilter


class Child(IDMixin, Base):
    __tablename__ = 'children'

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id'), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergarten_groups.id'), nullable=False)
    medicine_card_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey('medicine_cards.id'), nullable=True, unique=True
    )
    personal_acc: Mapped[str | None] = mapped_column(String, nullable=True)
    current_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergarten_groups.id'), nullable=True)

    profile: Mapped[Profile] = relationship(Profile, uselist=False, lazy='selectin')
    group: Mapped[KindergartenGroup] = relationship(
        KindergartenGroup, uselist=False, lazy='selectin', foreign_keys=[group_id]
    )
    medicine_card: Mapped[MedicineCard] = relationship(MedicineCard, uselist=False, lazy='selectin')
    current_group: Mapped[KindergartenGroup] = relationship(
        KindergartenGroup, uselist=False, lazy='selectin', foreign_keys=[current_group_id]
    )

    morning_filters: Mapped[List['MorningFilter']] = relationship('MorningFilter', uselist=True, back_populates='child')
    child_parent: Mapped[List['ChildParent']] = relationship('ChildParent', uselist=True, back_populates='child')

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.middle_name} {self.profile.last_name}'
