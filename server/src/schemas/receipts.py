from pydantic import BaseModel

from src.enums.receipt import ReceiptType, ReceiptStatus


class KindergartenSchema(BaseModel):
    class Config:
        from_attributes = True

    id: str
    name: str


class ProfileSchema(BaseModel):
    class Config:
        from_attributes = True

    first_name: str
    middle_name: str
    last_name: str


class ChildSchema(BaseModel):
    class Config:
        from_attributes = True

    id: str
    profile: ProfileSchema


class ReceiptSchema(BaseModel):
    class Config:
        from_attributes = True

    id: int
    amount: int
    type: ReceiptType
    status: ReceiptStatus
    kindergarten: KindergartenSchema


class CreateReceiptSchema(BaseModel):
    amount: int
    child_id: int
    type: ReceiptType


class SBPPaymentSchema(BaseModel):
    class Config:
        from_attributes = True

    link: str
    receipt: ReceiptSchema
