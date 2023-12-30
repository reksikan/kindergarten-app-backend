from datetime import date

from pydantic import BaseModel

from src.common.phone import RUPhoneNumber
from src.enums.confirm import ConfirmType
from src.enums.gender import Gender


class Profile(BaseModel):
    first_name: str
    last_name: str
    first_name: str
    middle_name: str
    last_name: str
    birthdate: date
    gender: Gender

    class Config:
        from_attributes = True


class Staff(BaseModel):
    profile: Profile

    class Config:
        from_attributes = True


class Parent(BaseModel):
    profile: Profile

    class Config:
        from_attributes = True


class Phone(BaseModel):
    phone: RUPhoneNumber

    class Config:
        from_attributes = True


class AccountMeResponse(BaseModel):
    id: int
    staff: Staff | None
    parent: Parent | None

    class Config:
        from_attributes = True


class NewParentRequest(BaseModel):
    phone: Phone
    parent: Parent

    class Config:
        from_attributes = True


class NewStaffRequest(BaseModel):
    phone: Phone
    staff: Staff

    class Config:
        from_attributes = True


class NewAccountResponse(NewParentRequest):
    password: str

    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_type: ConfirmType


class ChangePhone(BaseModel):
    password: str
    new_phone: RUPhoneNumber
    confirm_type: ConfirmType


class CodeConfirm(BaseModel):
    code: str


class RestoreAccount(BaseModel):
    phone: RUPhoneNumber
    confirm_type: ConfirmType


class RestoreAccountSetPassword(BaseModel):
    new_password: str
    code: str
