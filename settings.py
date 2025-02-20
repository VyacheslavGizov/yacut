import os
import re
import string
from math import factorial


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


ORIGINAL_URL_MAX_LENGTH = 1024
SHORT_LINK_MAX_LENGTH = 16
AUTOGEN_SHORT_LINK_LEN = 6
SHORT_LINK_ALPFABET = string.ascii_letters + string.digits
LEN = len(SHORT_LINK_ALPFABET)

SHORT_LINK_PATTERN = f'^[{SHORT_LINK_ALPFABET}]+$'
ORIGINAL_URL_PATTERN = re.compile(
    r'^[a-z]+://[^\/\?:]+([0-9]+)?(\/.*?)?(\?.*)?$', re.IGNORECASE)

GENERATION_ATTEMPTS_LIMIT = 500
