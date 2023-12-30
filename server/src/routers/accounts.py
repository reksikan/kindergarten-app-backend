from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from src.api.security import SecurityMiddleware
from src.db.models.account import Account
from src.routers.base import BaseRouter, add_route
from src.schemas.accounts import AccountMeResponse, NewParentRequest, NewAccountResponse, ChangePassword, CodeConfirm, \
    ChangePhone, RestoreAccount, RestoreAccountSetPassword, NewStaffRequest


class AccountsRouter(BaseRouter):
    _router = APIRouter(prefix='/accounts', tags=['accounts'])
    endpoints = []

    @add_route(
        endpoints,
        '/me',
        response_model=AccountMeResponse,
        dependencies=[SecurityMiddleware()],
    )
    async def get_me_info(self, request: Request):
        return request.state.account

    @add_route(
        endpoints,
        '/create/parent',
        methods=['POST'],
        response_model=NewAccountResponse,
        dependencies=[SecurityMiddleware(admin_available=True, staff_available=True)],
    )
    async def create_parent(self, body: NewParentRequest):
        if await self._db_manager.accounts.account_exits_with_phone(body.phone.phone):
            raise HTTPException(409, 'This number already used')

        password = SecurityMiddleware.create_password()
        new_account = await self._db_manager.accounts.create_new_account(
            phone_number=body.phone.phone,
            first_name=body.parent.profile.first_name,
            middle_name=body.parent.profile.middle_name,
            last_name=body.parent.profile.last_name,
            birthdate=body.parent.profile.birthdate,
            gender=body.parent.profile.gender.value,
            hashed_password=SecurityMiddleware.hash_password(password)
        )
        new_account.password = password
        return new_account

    @add_route(
        endpoints,
        '/create/staff',
        methods=['POST'],
        response_model=NewAccountResponse,
        dependencies=[SecurityMiddleware(admin_available=True)],
    )
    async def create_staff(self, body: NewStaffRequest):
        if await self._db_manager.accounts.account_exits_with_phone(body.phone.phone):
            raise HTTPException(409, 'This number already used')

        password = SecurityMiddleware.create_password()
        new_account = await self._db_manager.accounts.create_new_account(
            phone_number=body.phone.phone,
            first_name=body.staff.profile.first_name,
            middle_name=body.staff.profile.middle_name,
            last_name=body.staff.profile.last_name,
            birthdate=body.staff.profile.birthdate,
            gender=body.staff.profile.gender.value,
            hashed_password=SecurityMiddleware.hash_password(password),
            is_staff=True,
        )
        new_account.password = password
        return new_account

    @add_route(
        endpoints,
        path='/password/change',
        methods=['POST'],
        dependencies=[SecurityMiddleware()],
    )
    async def password_change(self, body: ChangePassword, request: Request):
        account: Account = request.state.account
        if body.old_password == body.new_password:
            raise HTTPException(status_code=422, detail='Passwords must be different')

    @add_route(
        endpoints,
        path='/password/change/confirm',
        methods=['POST'],
        dependencies=[SecurityMiddleware()],
    )
    async def password_change_confirm(self, body: CodeConfirm):
        pass

    @add_route(
        endpoints,
        path='/phone/change',
        methods=['POST'],
        dependencies=[SecurityMiddleware()]
    )
    async def phone_change(self, body: ChangePhone):
        pass

    @add_route(
        endpoints,
        path='/phone/change/confirm',
        methods=['POST'],
        dependencies=[SecurityMiddleware()],
    )
    async def phone_change_confirm(self, body: CodeConfirm):
        pass

    @add_route(
        endpoints,
        path='/restore',
        methods=['POST'],
    )
    async def restore_account(self, body: RestoreAccount):
        pass

    @add_route(
        endpoints,
        path='/restore/check_code',
        methods=['POST'],
    )
    async def restore_account_check_code(self, body: CodeConfirm):
        pass

    @add_route(
        endpoints,
        path='/restore/set_password',
        methods=['POST'],
    )
    async def restore_account_set_password(self, body: RestoreAccountSetPassword):
        pass