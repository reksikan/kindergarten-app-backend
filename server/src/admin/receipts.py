from sqladmin import ModelView

from src.db.models.receipt import Receipt


class ReceiptAdmin(ModelView, model=Receipt):
    column_list = [Receipt.id]

