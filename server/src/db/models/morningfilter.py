from datetime import datetime

from sqlalchemy import Float, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, IDMixin, CreatedAtMixin
from .child import Child
from .yawn import Yawn
from .defecation import Defecation
from .skincovering import SkinCovering
from .staff import Staff
from src.enums.morning_filter_status import MorningFilterStatus


class MorningFilter(IDMixin, CreatedAtMixin, Base):
    __tablename__ = 'morning_filters'

    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    note: Mapped[str | None] = mapped_column(String, nullable=True)
    child_id: Mapped[int] = mapped_column(Integer, ForeignKey('children.id'), nullable=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    confirmed_by_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('staff.id'), nullable=True)
    status: Mapped[MorningFilterStatus] = mapped_column(
        Enum(*[v.value for v in MorningFilterStatus], name='morning_filter_status'), nullable=False
    )

    yawn_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('yawns.id'), nullable=True)
    defecation_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('defecations.id'), nullable=True)
    skin_covering_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('skin_coverings.id'), nullable=True)

    child: Mapped[Child] = relationship(Child, uselist=False, lazy='selectin')
    yawn: Mapped[Yawn | None] = relationship(Yawn, uselist=False, lazy='selectin')
    defecation: Mapped[Defecation | None] = relationship(Defecation, uselist=False, lazy='selectin')
    skin_covering: Mapped[SkinCovering | None] = relationship(SkinCovering, uselist=False, lazy='selectin')
    confirmed_by: Mapped[Staff | None] = relationship(Staff, uselist=False, lazy='selectin')

    def __str__(self):
        return f'{self.child} - {self.confirmed_at}'
