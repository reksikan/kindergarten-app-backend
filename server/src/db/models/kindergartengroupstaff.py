from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, CreatedAtMixin, Base
from .staff import Staff
from .kindergartengroup import KindergartenGroup


class KindergartenGroupStaff(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'kindgarten_groups_staff'

    kindergarten_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergarten_groups.id'), nullable=False)
    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey('staff.id'), nullable=False)

    kindergarten_group: Mapped[KindergartenGroup] = relationship(KindergartenGroup, uselist=False, lazy='select')
    staff: Mapped[Staff] = relationship(Staff, uselist=False, lazy='select')

    def __str__(self):
        return f'{self.kindergarten_group_id} - {self.staff_id}'
