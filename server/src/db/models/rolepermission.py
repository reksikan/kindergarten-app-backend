from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, CreatedAtMixin, Base
from .role import Role
from .permission import Permission


class RolePermission(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'roles_permissions'

    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey('permissions.id'), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), nullable=False)

    permission: Mapped[Permission] = relationship(Permission, uselist=False, lazy='select')
    role: Mapped[Role] = relationship(Role, uselist=False, lazy='select')

    def __str__(self):
        return f'{self.permission_id} - {self.role_id}'
