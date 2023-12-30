from sqladmin import ModelView

from src.db.models.staffrole import StaffRole


class StaffRolAedmin(ModelView, model=StaffRole):
    column_list = [StaffRole.id, StaffRole.staff_id, StaffRole.role_id]
