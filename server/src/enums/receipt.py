from enum import Enum


class ReceiptType(Enum):
    FEE = 'fee'
    SERVICES = 'services'


class ReceiptStatus(Enum):
    NOT_PAID = 'not_paid'
    PAID = 'paid'
