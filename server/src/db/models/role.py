from typing import TYPE_CHECKING, List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin
from .kindergarten import Kindergarten

if TYPE_CHECKING:
    from .rolepermission import RolePermission
    from .staffrole import StaffRole


class Role(IDMixin, Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String, nullable=False)
    kindergarten_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergartens.id'), nullable=False)

    kindergarten: Mapped[Kindergarten] = relationship(Kindergarten, uselist=False, lazy='selectin')

    staff_roles: Mapped[List['StaffRole']] = relationship('StaffRole', uselist=True, lazy='select', back_populates='role')
    roles_permissions: Mapped[List['RolePermission']] = relationship(
        'RolePermission', uselist=True, lazy='select', back_populates='role'
    )

    def __str__(self):
        return f'{self.name}'
