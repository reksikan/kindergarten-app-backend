from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IDMixin, Base
from .diseasegroup import DiseaseGroup

if TYPE_CHECKING:
    from .medicinecarddisease import MedicineCardDisease


class Disease(IDMixin, Base):
    __tablename__ = 'diseases'

    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('diseases_groups.id'), nullable=True)

    group: Mapped[DiseaseGroup] = relationship(DiseaseGroup, uselist=False, lazy='selectin')

    medicine_card_disease: Mapped['MedicineCardDisease'] = relationship(
        'MedicineCardDisease', uselist=False, lazy='selectin', back_populates='disease'
    )

    def __str__(self):
        return self.name
