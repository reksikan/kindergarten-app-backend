from typing import List, Type

from fastapi import FastAPI

from src.api.admin import AdminInterface
from src.db.manager import DBManager
from src.routers.base import BaseRouter
from src.routers.accounts import AccountsRouter
from src.routers.checks import CheckRouter
from src.routers.morning_filter import MorningFilterClass
from src.routers.receipts import ReceiptRouter
from src.routers.tokens import TokenRouter
from src.services.manager import ServiceManager
from settings import DEBUG


class HTTPServer:
    _app = FastAPI(
        debug=DEBUG,
    )
    router_classes: List[Type[BaseRouter]] = [
        AccountsRouter,
        TokenRouter,
        ReceiptRouter,
        CheckRouter,
        MorningFilterClass,
    ]

    def __init__(self, db_manager: DBManager, service_manager: ServiceManager):
        self._db_manager = db_manager
        self._app.get('/ping', include_in_schema=False)(self._ping)
        for router_class in self.router_classes:
            self._app.include_router(router_class(db_manager, service_manager).router)

        self._admin_interface = AdminInterface(db_manager.engine, self._app)

    @staticmethod
    def _ping():
        return "OK"

    @property
    def app(self) -> FastAPI:
        return self._app
