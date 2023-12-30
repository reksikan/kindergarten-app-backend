from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, CreatedAtMixin, Base
from .role import Role
from .staff import Staff


class StaffRole(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'staff_roles'

    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey('staff.id'), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), nullable=False)

    staff: Mapped[Staff] = relationship(Staff, uselist=False, lazy='select')
    role: Mapped[Role] = relationship(Role, uselist=False, lazy='select')

    def __str__(self):
        return f'{self.staff_id} - {self.role_id}'
