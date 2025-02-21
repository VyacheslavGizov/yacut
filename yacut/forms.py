from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from .models import NONUNIQUE_SHORT, URLMap
from settings import (
    ORIGINAL_URL_MAX_LENGTH,
    SHORT_MAX_LENGTH,
    SHORT_PATTERN
)


LENGTH_MESSAGE = 'Максимальная длина ссылки до %(max)d символов!'
REQUIRED_MESSAGE = 'Это обязательное поле!'
WRONG_URL = 'Недопустимый фомат URL!'
WRONG_SHORT = ('Недопустимое имя короткой ссылки! Разрешены '
               'заглавные и прописные латинские буквы, цифры от 0 до 9')
ORIGINAL_URL_LABEL = 'Длинная ссылка'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
SEND = 'Создать'


class URLShortenerForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_URL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_MESSAGE),
            Length(max=ORIGINAL_URL_MAX_LENGTH, message=LENGTH_MESSAGE),
            URL(require_tld=False, message=WRONG_URL)
        ]
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Optional(),
            Length(max=SHORT_MAX_LENGTH, message=LENGTH_MESSAGE),
            Regexp(SHORT_PATTERN, message=WRONG_SHORT)
        ]
    )
    submit = SubmitField(SEND)

    def validate_custom_id(form, field):
        if URLMap.get_record(short=field.data):
            raise ValidationError(NONUNIQUE_SHORT)
