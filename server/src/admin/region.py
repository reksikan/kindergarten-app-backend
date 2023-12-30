from sqladmin import ModelView

from src.db.models.region import Region


class RegionAdmin(ModelView, model=Region):
    column_list = [Region.id]

