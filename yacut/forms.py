from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp


LENGTH_MESSAGE = 'Допустимая длина ссылки: от %(min)d до %(max)d символов!'
REQUIRED_MESSAGE = 'Это обязательное поле!'
WRONG_URL_FORMAT = 'Недопустимый фомат URL!'
WRONG_SHORT_URL = ('Допускаются: заглавные и прописные латинские '
                   'буквы, цифры от 1 до 9!')


class URLShortenerForm(FlaskForm):
    original = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message=REQUIRED_MESSAGE),
            Length(1, 256, message=LENGTH_MESSAGE),
            URL(require_tld=False, message=WRONG_URL_FORMAT)
        ]
    )
    short = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16, message=LENGTH_MESSAGE),
            Regexp(r'[A-Za-z0-9]', message=WRONG_SHORT_URL)  # хз какая регулярка, но она нужна
        ]
    )
    submit = SubmitField('Создать')
