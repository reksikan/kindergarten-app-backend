from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin

if TYPE_CHECKING:
    from .childparent import ChildParent


class RelationDegree(IDMixin, Base):
    __tablename__ = 'relation_degrees'

    value: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)

    child_parent: Mapped[List['ChildParent']] = relationship('ChildParent', uselist=True, back_populates='relation')

    def __str__(self):
        return f'{self.title}: {self.value}'
