from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin

if TYPE_CHECKING:
    from .child import Child
    from .medicinecarddisease import MedicineCardDisease


class MedicineCard(IDMixin, Base):
    __tablename__ = 'medicine_cards'

    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    heigth: Mapped[int] = mapped_column(Integer, nullable=False)
    allergies: Mapped[List[str]] = mapped_column(ARRAY(String), server_default='{}', nullable=False)
    notes: Mapped[List[str]] = mapped_column(ARRAY(String), server_default='{}', nullable=False)

    child: Mapped['Child'] = relationship('Child', uselist=False, lazy='selectin', back_populates='medicine_card')
    medicine_card_diseases: Mapped[List['MedicineCardDisease']] = relationship(
        'MedicineCardDisease', uselist=True, lazy='selectin', back_populates='medicine_card'
    )

    def __str__(self):
        return f'{self.child}'
