from sqladmin import ModelView

from src.db.models.staff import Staff


class StaffAdmin(ModelView, model=Staff):
    column_list = [Staff.id]
