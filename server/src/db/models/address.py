from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin
from .country import Country
from .city import City
from .region import Region
from .profile import Profile

if TYPE_CHECKING:
    from .kindergarten import Kindergarten


class Address(IDMixin, Base):
    __tablename__ = 'addresses'

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('countries.id'), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey('regions.id'), nullable=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id'), nullable=True, unique=True)

    country: Mapped[Country] = relationship(Country, uselist=False, lazy='selectin')
    city: Mapped[City] = relationship(City, uselist=False, lazy='selectin')
    region: Mapped[Region] = relationship(Region, uselist=False, lazy='selectin')
    profile: Mapped[Profile] = relationship(Profile, uselist=False, lazy='select')

    kindergarten: Mapped['Kindergarten'] = relationship(
        'Kindergarten', uselist=False, lazy='selectin', back_populates='address'
    )

    def __str__(self):
        return f'{self.country} | {self.region} | {self.city}'
