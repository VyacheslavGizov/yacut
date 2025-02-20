from datetime import datetime
import random
import re

from flask import url_for

from . import db
from .exceptions import ValidationError, ShortGenerationError
from settings import (
    AUTOGEN_SHORT_LINK_LEN,
    ORIGINAL_URL_MAX_LENGTH,
    ORIGINAL_URL_PATTERN,
    SHORT_LINK_ALPFABET,
    SHORT_LINK_MAX_LENGTH,
    SHORT_LINK_PATTERN,
    GENERATION_ATTEMPTS_LIMIT
)


WRONG_LINK_MESSAGE = 'Недопустимое имя ссылки.'
DUPLICATE_SHORT_LINK = 'Предложенный вариант короткой ссылки уже существует.'
WRONG_ORIGINAL_URL = 'Указано недопустимое имя для длинной ссылки'
WRONG_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
GENERATION_ERROR = 'Не удалось сгенерировать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_LINK_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        for _ in range(GENERATION_ATTEMPTS_LIMIT):
            short = ''.join(random.choices(SHORT_LINK_ALPFABET,
                                           k=AUTOGEN_SHORT_LINK_LEN))
            if not URLMap.get_record_by_fields(short=short):
                return short
            raise ShortGenerationError(GENERATION_ERROR)

    # @staticmethod
    # def get_unique_short_id(length=AUTOGEN_SHORT_LINK_LENGTH):
    #     return ''.join(
    #         random.choice(SHORT_LINK_ALPFABET) for _ in range(length))

    @staticmethod
    def validate_link(pattern, link, max_length, message=WRONG_LINK_MESSAGE):
        if len(link) > max_length or not re.fullmatch(pattern, link):
            raise ValidationError(message)
        return link

    @classmethod
    def get_record_by_fields(model, **fields):  # или filter
        return model.query.filter_by(**fields).first()

    @classmethod
    def create(model, original, short=None):
        if short:
            if model.get_record_by_fields(short=short):
                raise ValidationError(DUPLICATE_SHORT_LINK)  # или дубликатошибка
            model.validate_link(
                link=short,
                pattern=SHORT_LINK_PATTERN,
                max_length=SHORT_LINK_MAX_LENGTH,
                message=WRONG_SHORT_URL
            )
        else:
            short = model.get_unique_short_id()
        model.validate_link(
            link=original,
            pattern=ORIGINAL_URL_PATTERN,
            max_length=ORIGINAL_URL_MAX_LENGTH,
            message=WRONG_ORIGINAL_URL
        )
        url_map = model(short=short, original=original)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def get_short_url(self):
        return url_for('redirect_view', short=self.short, _external=True)

    @classmethod
    def get_record_or_404(model, **fields):
        return model.query.filter_by(**fields).first_or_404()
