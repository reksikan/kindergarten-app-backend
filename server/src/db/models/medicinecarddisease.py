from datetime import date

from sqlalchemy import Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin
from .disease import Disease
from .medicinecard import MedicineCard


class MedicineCardDisease(IDMixin, Base):
    __tablename__ = 'medicine_cards_diseases'

    medicine_card_id: Mapped[int] = mapped_column(Integer, ForeignKey('medicine_cards.id'), nullable=False)
    disease_id: Mapped[int] = mapped_column(Integer, ForeignKey('diseases.id'), nullable=False)
    started_at: Mapped[date] = mapped_column(Date, nullable=False)
    finished_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_chronic: Mapped[bool] = mapped_column(Boolean, nullable=False)

    medicine_card: Mapped[MedicineCard] = relationship(MedicineCard, lazy='select', uselist=False)
    disease: Mapped[Disease] = relationship(Disease, lazy='select', uselist=False)

    def __str__(self):
        return f'{self.medicine_card} - {self.disease}'
