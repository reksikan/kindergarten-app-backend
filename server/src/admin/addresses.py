from sqladmin import ModelView

from src.db.models.address import Address


class AddressAdmin(ModelView, model=Address):
    column_list = [Address.id]

