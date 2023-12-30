from phonenumbers import PhoneNumberFormat
from pydantic_extra_types.phone_numbers import PhoneNumber


class RUPhoneNumber(PhoneNumber):
    phone_format = 'INTERNATIONAL'

