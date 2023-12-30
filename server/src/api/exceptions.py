from fastapi import HTTPException


class AccessDeniedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail='Access denied for this action')


class AccountNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail='Account not found')
