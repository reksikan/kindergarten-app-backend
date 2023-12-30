from fastapi import Request

from src.db.models.users import User


class AuthedRequest(Request):
    user: User
