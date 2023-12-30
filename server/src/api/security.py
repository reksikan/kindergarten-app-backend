import string
from datetime import datetime, timedelta
from typing import List, Annotated
from random import randint, choice

from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.api.exceptions import AccessDeniedError, AccountNotFound
from src.db.manager import DBManager
from src.db.models.account import Account
from src.db.models.permission import Permission
from src.enums.permissions import PermissionAction,  PermissionAccess
from settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)


class SecurityMiddleware:
    __pwd_password = CryptContext(schemes=["bcrypt"], deprecated="auto")
    allowed_symbols = string.ascii_letters + '_-*#'

    def __init__(
        self,
        parents_available: bool = False,
        staff_available: bool = False,
        admin_available: bool = False,
        access_action: PermissionAction = None,
        access_type: PermissionAccess = None,
        db_manager: DBManager | None = None
    ):
        self.__db_manager = db_manager
        self._access_action = access_action
        self._access_type = access_type
        self._parents_available = parents_available
        self._staff_available = staff_available
        self._admin_available = admin_available

    def setup(self, db_manager: DBManager):
        self.__db_manager = db_manager

    @property
    def _just_auth(self):
        return not (self._parents_available or self._admin_available or self._staff_available)

    @property
    def _db_manager(self):
        if self.__db_manager is None:
            raise NotImplementedError
        return self.__db_manager

    @classmethod
    def create_password(cls):
        return ''.join(
            [choice(cls.allowed_symbols) for _ in range(randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH))]
        )

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.__pwd_password.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.__pwd_password.hash(password)

    async def get_account(self, phone_number: str) -> Account | None:
        return await self._db_manager.accounts.get_by_phone_number(phone_number)

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def refresh_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            phone_number: str = payload['sub']
            if phone_number is None:
                raise jwt.JWTError()
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, 'Token expired')
        except jwt.JWTError:
            raise HTTPException(401, detail='Bad token')

        user = await self.get_account(phone_number)
        if user is None:
            raise HTTPException(401, detail='User not found')

        return self.create_refresh_token({'sub': phone_number})

    async def __call__(
        self,
        request: Request,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token/login'))]
    ):

        if 'Authorization' not in request.headers:
            raise HTTPException(status_code=401, detail='No Authorization header')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            phone_number: str = payload['sub']
            if phone_number is None:
                raise jwt.JWTError()
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, 'Token expired')
        except jwt.JWTError:
            raise HTTPException(401, detail='Bad token')

        account = await self.get_account(phone_number)
        if account is None:
            raise AccountNotFound()
        request.state.account = account

        if self._just_auth:
            return

        if self._parents_available and account.parent is not None and account.parent.is_active:
            return

        if account.staff is None or not account.staff.is_active:
            raise AccessDeniedError()

        if self._admin_available and account.staff.is_admin:
            return

        staff_permissions: List[Permission] = account.staff.permissions
        for permission in staff_permissions:
            if (
                (self._access_type is None or permission.access == self._access_type)
                and (self._access_action is None or permission.action == self._access_action)
            ):
                return

        raise AccessDeniedError()
