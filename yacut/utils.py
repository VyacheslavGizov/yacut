import random
import string
import re
from http import HTTPStatus

from .error_handlers import APIExceptions

SHORT_ID_ALPFABET = string.ascii_letters + string.digits

MISSMATCH_MESSAGE = 'Не соответствует шаблону.'


def get_unique_short_id(length=6, alpfabet=None):
    alpfabet = SHORT_ID_ALPFABET if alpfabet is None else alpfabet
    return ''.join(random.choice(alpfabet) for _ in range(length))


def get_records(model, **fields):
    return model.query.filter_by(**fields).all()


def write_to_databese(db, model, **fields):
    record = model(**fields)
    db.session.add(record)
    db.session.commit()
    return record


def regex_validation(pattern, string, message=MISSMATCH_MESSAGE):
    if re.fullmatch(pattern, string):
        return string
    else:
        raise APIExceptions(message, HTTPStatus.BAD_REQUEST)  # Пока так, потом пересмотреть функцию, и эти вещи возвращать в вызывающем коде 
