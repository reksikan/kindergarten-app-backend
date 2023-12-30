from sqladmin import ModelView

from src.db.models.phone import Phone


class PhoneAdmin(ModelView, model=Phone):
    column_list = [Phone.id, Phone.phone]