from sqladmin import ModelView

from src.db.models.child import Child


class ChildAdmin(ModelView, model=Child):
    column_list = [Child.id]
