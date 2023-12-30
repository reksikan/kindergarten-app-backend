from sqladmin import ModelView

from src.db.models.profile import Profile


class ProfileAdmin(ModelView, model=Profile):
    column_list = [Profile.id, Profile.first_name, Profile.middle_name]
