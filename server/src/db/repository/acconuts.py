from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import contains_eager, selectinload

from .base import BaseRepository
from ..models.account import Account
from ..models.parent import Parent
from ..models.password import Password
from ..models.phone import Phone
from ..models.profile import Profile
from ..models.role import Role
from ..models.staff import Staff
from ..models.staffrole import StaffRole
from src.enums.gender import Gender


class AccountRepository(BaseRepository):

    async def get_by_phone_number(self, phone_number: str) -> Account | None:
        async with self._client.session() as session:
            return (await session.scalars(
                select(Account)
                .join(Account.phone)
                .join(Account.passwords)
                .order_by(Password.account_id.asc(), Password.created_at.desc())
                .distinct(Password.account_id)
                .where(
                    Phone.phone == phone_number
                )
                .options(
                    contains_eager(Account.phone),
                    contains_eager(Account.passwords)
                )
            )).unique().one_or_none()

    async def create_new_account(
        self,
        phone_number: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        birthdate: date,
        gender: Gender,
        hashed_password: str,
        is_staff: bool = False,
    ) -> Account:
        async with self._client.session() as session:
            phone = Phone(phone=phone_number)
            session.add(phone)

            account = Account(phone=phone)
            profile = Profile(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                birthdate=birthdate.isoformat(),
                gender=gender,
            )
            session.add(profile)
            session.add(account)

            session.add(Password(account=account, hash=hashed_password, is_temporary=True))
            if is_staff:
                session.add(Parent(profile=profile, account=account))
            else:
                session.add(Staff(profile=profile, account=account))

            await session.flush()
        return await self.get_by_phone_number(phone_number)

    async def account_exits_with_phone(self, phone_number) -> bool:

        async with self._client.session() as session:
            return (await session.scalar(
                select(
                    select(Account)
                    .join(Account.phone)
                    .join(Account.passwords)
                    .order_by(Password.account_id.asc(), Password.created_at.desc())
                    .distinct(Password.account_id)
                    .where(
                        Phone.phone == phone_number
                    )
                    .exists()
                   )
                )
            )