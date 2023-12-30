from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, IDMixin
from .account import Account
from .profile import Profile
from .kindergarten import Kindergarten
from .job import Job

if TYPE_CHECKING:
    from .kindergartengroupstaff import KindergartenGroupStaff
    from .staffrole import StaffRole
    from .morningfilter import MorningFilter
    from .permission import Permission


class Staff(Base, IDMixin):
    __tablename__ = 'staff'

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=False, unique=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id'), nullable=False, unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    waiting_for_approve: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    kindergarten_id: Mapped[int] = mapped_column(Integer, ForeignKey('kindergartens.id'), nullable=False)
    job_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=True)

    account: Mapped[Account] = relationship(Account, uselist=False, lazy='selectin')
    profile: Mapped[Profile] = relationship(Profile, uselist=False, lazy='selectin')
    kindergarten: Mapped[Kindergarten] = relationship(Kindergarten, uselist=False, lazy='selectin')
    job: Mapped[Job | None] = relationship(Job, uselist=False, lazy='selectin')

    kindergarten_group_staff: Mapped[List['KindergartenGroupStaff']] = relationship(
        'KindergartenGroupStaff', uselist=True, lazy='select', back_populates='staff'
    )
    staff_roles: Mapped[List['StaffRole']] = relationship(
        'StaffRole', uselist=True, lazy='select', back_populates='staff'
    )
    confirmed_morning_filters: Mapped[List['MorningFilter']] = relationship(
        'MorningFilter', uselist=True, lazy='select', back_populates='confirmed_by'
    )

    @property
    def permissions(self) -> List['Permission']:
        permissions = []
        for staff_role in self.staff_roles:
            for role_permission in staff_role.role.roles_permissions:
                permissions.append(role_permission.permission)
        return permissions

    def __str__(self):
        return f'{self.profile}'
