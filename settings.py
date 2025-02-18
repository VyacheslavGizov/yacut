import os
import re
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


ORIGINAL_URL_MAX_LENGTH = 256
SHORT_LINK_MAX_LENGTH = 16
AUTOGEN_SHORT_LINK_LENGTH = 6

SHORT_LINK_PATTERN = r'^[a-zA-Z0-9]+$'
ORIGINAL_URL_PATTERN = re.compile(
    r'^[a-z]+://[^\/\?:]+([0-9]+)?(\/.*?)?(\?.*)?$', re.IGNORECASE)
SHORT_LINK_ALPFABET = string.ascii_letters + string.digits
