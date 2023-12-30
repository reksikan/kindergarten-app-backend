from src.db.client import DBClient


class BaseRepository:
    _client: DBClient

    def __init__(self, client: DBClient):
        self._client = client
