import random

from .exceptions import DataBaseError
from settings import AUTOGEN_SHORT_LINK_LENGTH, SHORT_LINK_ALPFABET


MISSMATCH_MESSAGE = 'Не соответствует шаблону.'
DB_ERROR_MESSAGE = 'При попытке записи в базу данных возникла ошибка: {error}'


def get_unique_short_id(length=AUTOGEN_SHORT_LINK_LENGTH, alpfabet=None):
    alpfabet = SHORT_LINK_ALPFABET if alpfabet is None else alpfabet
    return ''.join(random.choice(alpfabet) for _ in range(length))


def get_records(model, **fields):
    return model.query.filter_by(**fields).all()


def write_to_databese(db, model, **fields):
    try:
        record = model(**fields)
        db.session.add(record)
        db.session.commit()
    except Exception as error:
        raise DataBaseError(DB_ERROR_MESSAGE.format(error=error))
    return record
