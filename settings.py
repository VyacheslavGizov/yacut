import os
import re
from string import ascii_letters, digits


EXTRACT_FUNCTION = 'redirect_view'

ORIGINAL_URL_MAX_LENGTH = 1024
SHORT_MAX_LENGTH = 16
GENERATED_SHORT_MAX_LENGTH = 6

ALLOWED_CHARACTERS = ascii_letters + digits
SHORT_PATTERN = f'^[{ALLOWED_CHARACTERS}]+$'
ORIGINAL_URL_PATTERN = re.compile(
    r'^[a-z]+://[^\/\?:]+([0-9]+)?(\/.*?)?(\?.*)?$', re.IGNORECASE)

WAITING_TIME = 10  # Секунд


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
