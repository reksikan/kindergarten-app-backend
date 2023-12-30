from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm

from .base import BaseRouter, add_route
from src.api.security import SecurityMiddleware
from src.schemas.tokens import TokenResponse, RefreshTokenRequest


class TokenRouter(BaseRouter):
    _router = APIRouter(prefix='/token', tags=['tokens'])
    endpoints = []

    @add_route(
        endpoints,
        '/login',
        response_model=TokenResponse,
        methods=['POST'],
    )
    async def get_token(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        security = SecurityMiddleware(db_manager=self._db_manager)
        account = await security.get_account(form_data.username)
        if not account or not security.verify_password(form_data.password, account.passwords[0].hash):
            raise HTTPException(401, detail='Incorrect password')

        return TokenResponse(
            access_token=security.create_access_token({'sub': form_data.username}),
            refresh_token=security.create_refresh_token({'sub': form_data.username}),
            token_type='bearer',
        )

    @add_route(
        endpoints,
        '/refresh',
        methods=['POST'],
    )
    async def refresh_token(self, body: RefreshTokenRequest):
        security = SecurityMiddleware(db_manager=self._db_manager)
        new_access_token = await security.refresh_token(body.refresh_token)
        return Response(headers={'Authorization': 'Bearer {}'.format(new_access_token)})
