from sqladmin import ModelView

from src.db.models.account import Account
from src.db.models.phone import Phone


class AccountAdmin(ModelView, model=Account):
    column_list = [Account.id, Phone.phone]

