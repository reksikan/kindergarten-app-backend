from fastapi import APIRouter
from starlette.responses import FileResponse

from .base import BaseRouter, add_route
from ..enums.file_extensions import FileExtensions


class MorningFilterClass(BaseRouter):
    _router = APIRouter(prefix='/morning_filter', tags=['morning_filters'])
    endpoints = []

    @add_route(
        endpoints,
        '/',
        methods=['GET'],
    )
    async def morning_filters_list(self):
        pass

    @add_route(
        endpoints,
        '/{filter_id}',
        methods=['GET'],
    )
    async def get_filter_by_id(self, filter_id: int):
        pass

    @add_route(
        endpoints,
        '/{filter_id}/export',
        response_class=FileResponse,
        methods=['GET'],
    )
    async def export_filter(self, filter_id: int, file_ext: FileExtensions):
        pass

    @add_route(
        endpoints,
        '/',
        methods=['POST'],
    )
    async def create_filter(self, body):
        pass

    @add_route(
        endpoints,
        '/{filter_id}',
        methods=['PATCH'],
    )
    async def update_filter(self, filter_id: int, body):
        pass

