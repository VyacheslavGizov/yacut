from datetime import datetime
from random import choices
from re import fullmatch

from flask import url_for

from . import db
from settings import (
    ALLOWED_CHARACTERS,
    ATTEMPTS_LIMIT,
    EXTRACT_FUNCTION,
    GENERATED_SHORT_MAX_LENGTH,
    ORIGINAL_URL_MAX_LENGTH,
    PATTERN,
    SHORT_MAX_LENGTH,
)


WRONG_LINK = 'Недопустимое имя ссылки.'
NONUNIQUE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
WRONG_ORIGINAL_URL = 'Указано недопустимое имя для длинной ссылки'
WRONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_GENERATION_ERROR = ('Не удалось сгенерировать короткую ссылку. '
                          f'Сделано попыток: {ATTEMPTS_LIMIT}')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    class ShortGenerationError(Exception):
        pass

    @staticmethod
    def get_unique_short_id():
        for _ in range(ATTEMPTS_LIMIT):
            short = ''.join(choices(
                ALLOWED_CHARACTERS, k=GENERATED_SHORT_MAX_LENGTH))
            if not URLMap.get(short):
                return short
        raise URLMap.ShortGenerationError(SHORT_GENERATION_ERROR)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def create(original, short=None, validate=True):
        if short and validate:
            if len(short) > SHORT_MAX_LENGTH or not fullmatch(PATTERN, short):
                raise ValueError(WRONG_SHORT)
            if URLMap.get(short):
                raise ValueError(NONUNIQUE_SHORT)
        if not short:
            short = URLMap.get_unique_short_id()
        if validate and len(original) > ORIGINAL_URL_MAX_LENGTH:
            raise ValueError(WRONG_ORIGINAL_URL)
        record = URLMap(short=short, original=original)
        db.session.add(record)
        db.session.commit()
        return record

    def get_short_url(self):
        return url_for(EXTRACT_FUNCTION, short=self.short, _external=True)
