from typing import List

from fastapi import APIRouter

from .base import BaseRouter, add_route
from src.schemas.checks import YawnSchema, SkinCoveringSchema, DefecationSchema


class CheckRouter(BaseRouter):
    _router = APIRouter(prefix='/checks', tags=['check-values'])
    endpoints = []

    @add_route(
        endpoints,
        '/yawn',
        methods=['GET'],
        response_model=List[YawnSchema],
    )
    async def yawn_list(self):
        pass

    @add_route(
        endpoints,
        '/defecation',
        methods=['GET'],
        response_model=List[DefecationSchema],
    )
    async def defecation_list(self):
        pass

    @add_route(
        endpoints,
        '/skin_covering',
        methods=['GET'],
        response_model=List[SkinCoveringSchema],
    )
    async def skin_covering_list(self):
        pass
