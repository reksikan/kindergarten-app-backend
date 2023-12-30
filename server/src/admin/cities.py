from sqladmin import ModelView

from src.db.models.city import City


class CityAdmin(ModelView, model=City):
    column_list = [City.id]

