from sqladmin import ModelView

from src.db.models.password import Password


class PasswordAdmin(ModelView, model=Password):
    column_list = [Password.id]

