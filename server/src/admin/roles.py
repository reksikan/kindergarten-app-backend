from sqladmin import ModelView

from src.db.models.role import Role


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id]