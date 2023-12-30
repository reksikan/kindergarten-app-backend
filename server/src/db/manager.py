import subprocess

from sqlalchemy.ext.asyncio import create_async_engine

from src.db.client import DBClient
from src.db.repository.acconuts import AccountRepository
from src.db.repository.children import ChildrenRepository
from src.db.repository.receipts import ReceiptRepository
from src.db.repository.sbp_payment import SBPPaymentRepository


class DBManager:

    def __init__(self, connection_url: str, need_migrations: bool = True):
        self._engine = create_async_engine(connection_url)
        if need_migrations:
            subprocess.run(
                'alembic upgrade head',
                check=True,
                shell=True
            )

        client = DBClient(self._engine)
        self._accounts = AccountRepository(client)
        self._receipts = ReceiptRepository(client)
        self._children = ChildrenRepository(client)
        self._sbp_payments = SBPPaymentRepository(client)

    @property
    def engine(self):
        return self._engine

    @property
    def accounts(self) -> AccountRepository:
        return self._accounts

    @property
    def receipts(self) -> ReceiptRepository:
        return self._receipts

    @property
    def children(self) -> ChildrenRepository:
        return self._children

    @property
    def sbp_payments(self) -> SBPPaymentRepository:
        return self._sbp_payments
