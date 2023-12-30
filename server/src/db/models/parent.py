from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base
from .account import Account
from .profile import Profile

if TYPE_CHECKING:
    from .childparent import ChildParent


class Parent(IDMixin, Base):
    __tablename__ = 'parents'

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=False, unique=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id'), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    work_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    job: Mapped[str | None] = mapped_column(String, nullable=True)
    place_of_work: Mapped[str | None] = mapped_column(String, nullable=True)

    account: Mapped[Account] = relationship(Account, uselist=False, lazy='selectin')
    profile: Mapped[Profile] = relationship(Profile, uselist=False, lazy='selectin')

    child_parent: Mapped[List['ChildParent']] = relationship(
        'ChildParent', uselist=True, lazy='select', back_populates='parent'
    )

    def __str__(self):
        return f'{self.profile}'
