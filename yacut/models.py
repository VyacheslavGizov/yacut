from datetime import datetime
from random import choices
from re import fullmatch
from time import time

from flask import url_for
from sqlalchemy.orm import validates

from . import db
from .exceptions import ShortGenerationError
from settings import (
    ALLOWED_CHARACTERS,
    EXTRACT_FUNCTION,
    GENERATED_SHORT_MAX_LENGTH,
    ORIGINAL_URL_MAX_LENGTH,
    ORIGINAL_URL_PATTERN,
    SHORT_MAX_LENGTH,
    SHORT_PATTERN,
    WAITING_TIME,
)


WRONG_LINK = 'Недопустимое имя ссылки.'
NONUNIQUE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
WRONG_ORIGINAL_URL = 'Указано недопустимое имя для длинной ссылки'
WRONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_GENERATION_ERROR = 'Не удалось сгенерировать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @validates('short')
    def validate_short(self, key, short):
        return URLMap.validate_link(
            link=short,
            pattern=SHORT_PATTERN,
            max_length=SHORT_MAX_LENGTH,
            message=WRONG_SHORT
        )

    @validates('original')
    def validate_original(self, key, original):
        return URLMap.validate_link(
            link=original,
            pattern=ORIGINAL_URL_PATTERN,
            max_length=ORIGINAL_URL_MAX_LENGTH,
            message=WRONG_ORIGINAL_URL
        )

    @staticmethod
    def validate_link(pattern, link, max_length, message=WRONG_LINK):
        if len(link) > max_length or not fullmatch(pattern, link):
            raise ValueError(message)
        return link

    @staticmethod
    def get_unique_short_id():
        start_time = time()
        while time() - start_time < WAITING_TIME:
            short = ''.join(choices(
                ALLOWED_CHARACTERS, k=GENERATED_SHORT_MAX_LENGTH))
            if not URLMap.get_record(short=short):
                return short
        else:
            raise ShortGenerationError(SHORT_GENERATION_ERROR)

    @classmethod
    def _get_filter_by(model, **fields):
        return model.query.filter_by(**fields)

    @classmethod
    def get_record(model, **fields):
        return model._get_filter_by(**fields).first()

    @classmethod
    def get_record_or_404(model, **fields):
        return model._get_filter_by(**fields).first_or_404()

    @classmethod
    def create(model, original, short=None):
        if short:
            if model.get_record(short=short):
                raise ValueError(NONUNIQUE_SHORT)
        else:
            short = model.get_unique_short_id()
        record = model(short=short, original=original)
        db.session.add(record)
        db.session.commit()
        return record

    def get_short_url(self):
        return url_for(EXTRACT_FUNCTION, short=self.short, _external=True)
