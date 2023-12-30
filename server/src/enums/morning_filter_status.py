from enum import Enum


class MorningFilterStatus(Enum):
    FILLED = 'filled'
    NOT_FILLED = 'not_filled'
    MISSING = 'missing'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
