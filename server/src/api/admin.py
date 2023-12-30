from sqladmin import Admin

from src.admin.accounts import AccountAdmin
from src.admin.addresses import AddressAdmin
from src.admin.cities import CityAdmin
from src.admin.countries import CountryAdmin
from src.admin.kindergartens import KindergartenAdmin
from src.admin.passwords import PasswordAdmin
from src.admin.permissions import PermissionAdmin
from src.admin.phones import PhoneAdmin
from src.admin.profiles import ProfileAdmin
from src.admin.region import RegionAdmin
from src.admin.rolepermission import RolePermissionAdmin
from src.admin.roles import RoleAdmin
from src.admin.staff import StaffAdmin
from src.admin.staffrole import StaffRolAedmin
from src.admin.receipts import ReceiptAdmin
from src.admin.children import ChildAdmin


class AdminInterface:
    def __init__(self, engine, app):
        self._admin_core = Admin(app, engine)
        self._admin_core.add_view(AccountAdmin)
        self._admin_core.add_view(AddressAdmin)
        self._admin_core.add_view(CityAdmin)
        self._admin_core.add_view(CountryAdmin)
        self._admin_core.add_view(KindergartenAdmin)
        self._admin_core.add_view(PasswordAdmin)
        self._admin_core.add_view(PermissionAdmin)
        self._admin_core.add_view(PhoneAdmin)
        self._admin_core.add_view(ProfileAdmin)
        self._admin_core.add_view(RegionAdmin)
        self._admin_core.add_view(RolePermissionAdmin)
        self._admin_core.add_view(RoleAdmin)
        self._admin_core.add_view(StaffAdmin)
        self._admin_core.add_view(StaffRolAedmin)
        self._admin_core.add_view(ReceiptAdmin)
        self._admin_core.add_view(ChildAdmin)

    @property
    def admin_core(self):
        return self._admin_core
