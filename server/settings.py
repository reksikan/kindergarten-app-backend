"""
settings.py - module containing list of config parameters
"""

import os

DEBUG = (os.getenv('DEBUG', 'True') == 'True')

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
POSTGRES_DB = os.getenv('POSTGRES_DB', 'kindergarten')
POSTGRES_CONNECT_STR = (
    f'postgresql+asyncpg://'
    f'{POSTGRES_USER}:'
    f'{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:'
    f'{POSTGRES_PORT}/'
    f'{POSTGRES_DB}'
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 4 * 24 * 60
PASSWORD_MAX_LENGTH = 16
PASSWORD_MIN_LENGTH = 8

SMS_SERVICE_URL = os.getenv('SMS_SERVICE_URL', 'localhost')

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_FROM = os.getenv('EMAIL_FROM', f'do_not_reply@{EMAIL_HOST}')
EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_TLS = (os.getenv('EMAIL_TLS', 'False') == 'True')
