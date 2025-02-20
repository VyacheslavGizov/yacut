from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp
from wtforms import ValidationError

from settings import (
    ORIGINAL_URL_MAX_LENGTH,
    SHORT_LINK_MAX_LENGTH,
    SHORT_LINK_PATTERN
)
from .models import URLMap


LENGTH_MESSAGE = 'Максимальная длина ссылки до %(max)d символов!'
REQUIRED_MESSAGE = 'Это обязательное поле!'
WRONG_URL_FORMAT = 'Недопустимый фомат URL!'
WRONG_SHORT_URL = ('Недопустимое имя короткой ссылки! Разрешены '
                   'заглавные и прописные латинские буквы, цифры от 0 до 9')
ORIGINAL_URL_LABEL = 'Длинная ссылка'
SHORT_LINK_LABEL = 'Ваш вариант короткой ссылки'
SEND = 'Создать'
DUPLICATE_SHORT_LINK = 'Предложенный вариант короткой ссылки уже существует.'


def exist_validation(form, field):
    if URLMap.get_record_by_fields(short=field.data):
        raise ValidationError(DUPLICATE_SHORT_LINK)


class URLShortenerForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_URL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_MESSAGE),
            Length(max=ORIGINAL_URL_MAX_LENGTH, message=LENGTH_MESSAGE),
            URL(require_tld=False, message=WRONG_URL_FORMAT)
        ]
    )
    custom_id = StringField(
        SHORT_LINK_LABEL,
        validators=[
            Optional(),
            Length(max=SHORT_LINK_MAX_LENGTH, message=LENGTH_MESSAGE),
            Regexp(SHORT_LINK_PATTERN, message=WRONG_SHORT_URL),
            exist_validation
        ]
    )
    submit = SubmitField(SEND)
    # добавить валидацию короткой ссылки по базе данных
