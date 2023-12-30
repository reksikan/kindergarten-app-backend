from enum import Enum


class PermissionAccess(Enum):
    READ = 'read'
    EDIT = 'edit'


class PermissionAction(Enum):
    CREATE_PARENT = 'create_parent'
    PAYMENTS = 'payments'
