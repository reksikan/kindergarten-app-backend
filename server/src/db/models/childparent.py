from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base
from .child import Child
from .parent import Parent
from .relationdegree import RelationDegree


class ChildParent(IDMixin, Base):
    __tablename__ = 'children_parents'

    parent_id: Mapped['int'] = mapped_column(Integer, ForeignKey('parents.id'), nullable=False)
    child_id: Mapped['int'] = mapped_column(Integer, ForeignKey('children.id'), nullable=False)
    relation_id: Mapped['int'] = mapped_column(Integer,ForeignKey('relation_degrees.id'), nullable=False)

    child: Mapped[Child] = relationship(Child, uselist=False, lazy='select')
    parent: Mapped[Parent] = relationship(Parent, uselist=False, lazy='select')
    relation: Mapped[RelationDegree] = relationship(RelationDegree, uselist=False, lazy='selectin')

    def __str__(self):
        return f'{self.child_id} - {self.parent_id}'
