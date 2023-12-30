"""
main.py - module containing entrypoint data for FastAPI
"""

from fastapi import FastAPI

from src.db.manager import DBManager
from src.api.http import HTTPServer
from settings import POSTGRES_CONNECT_STR
from src.services.manager import ServiceManager


def get_app() -> FastAPI:
    db_manager = DBManager(POSTGRES_CONNECT_STR)
    service_manager = ServiceManager()

    _app = HTTPServer(db_manager, service_manager).app

    return _app


app = get_app()
