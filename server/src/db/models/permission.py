from typing import TYPE_CHECKING, List

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base
from src.enums.permissions import PermissionAction, PermissionAccess

if TYPE_CHECKING:
    from .rolepermission import RolePermission


class Permission(IDMixin, Base):
    __tablename__ = 'permissions'

    action: Mapped[PermissionAction] = mapped_column(
        Enum(*[v.value for v in PermissionAction], name='permission_action'), nullable=False
    )
    access: Mapped[PermissionAccess] = mapped_column(
        Enum(*[v.value for v in PermissionAccess], name='permission_access'), nullable=False
    )

    roles_permissions: Mapped[List['RolePermission']] = relationship(
        'RolePermission', uselist=True, lazy='select', back_populates='permission'
    )

    def __str__(self):
        return f'{self.action}: {self.access}'
