from sqladmin import ModelView

from src.db.models.kindergarten import Kindergarten


class KindergartenAdmin(ModelView, model=Kindergarten):
    column_list = [Kindergarten.id, Kindergarten.name]
