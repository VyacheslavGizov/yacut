import re

from .exceptions import ValidationError


WRONG_LINK_MESSAGE = 'Недопустимое имя ссылки.'


def link_validator(pattern, link, max_length, message=WRONG_LINK_MESSAGE):
    if len(link) > max_length or not re.fullmatch(pattern, link):
        raise ValidationError(message)
    return link
