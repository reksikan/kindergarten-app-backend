from sqladmin import ModelView

from src.db.models.country import Country


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.id]

