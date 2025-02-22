import os
from re import escape
from string import ascii_letters, digits


EXTRACT_FUNCTION = 'redirect_view'

ORIGINAL_URL_MAX_LENGTH = 1024
SHORT_MAX_LENGTH = 16
GENERATED_SHORT_MAX_LENGTH = 6
ATTEMPTS_LIMIT = 500

ALLOWED_CHARACTERS = ascii_letters + digits
PATTERN = f'^[{escape(ALLOWED_CHARACTERS)}]+$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
