from sqladmin import ModelView

from src.db.models.permission import Permission


class PermissionAdmin(ModelView, model=Permission):
    column_list = [Permission.id, Permission.action, Permission.access]

