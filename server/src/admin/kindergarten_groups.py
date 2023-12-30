from sqladmin import ModelView

from src.db.models.kindergartengroup import KindergartenGroup


class KindergartenAdmin(ModelView, model=KindergartenGroup):
    column_list = [KindergartenGroup.id, KindergartenGroup.name]
