from sqladmin import ModelView

from src.db.models.rolepermission import RolePermission


class RolePermissionAdmin(ModelView, model=RolePermission):
    column_list = [RolePermission.id, RolePermission.permission_id, RolePermission.permission_id]
