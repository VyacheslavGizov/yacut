from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import APIException
from .exceptions import DataBaseError, EmptyError, ValidationError
from .models import URLMap
from .utils import get_records, get_unique_short_id, write_to_databese
from .validators import link_validator
from .views import get_exists_short_for_original
from settings import (
    ORIGINAL_URL_MAX_LENGTH,
    ORIGINAL_URL_PATTERN,
    SHORT_LINK_MAX_LENGTH,
    SHORT_LINK_PATTERN
)


EMPTY_REQUEST_BODY = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
WRONG_ORIGINAL_URL = 'Указано недопустимое имя для длинной ссылки'
WRONG_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT_LINK = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_LINK_NOT_FOUND = 'Указанный id не найден'
SERVER_ERROR = 'Ошибка сервера.'

ORIGINAL_URL_KEY = 'url'
SHORT_LINK_KEY = 'custom_id'



@app.route('/api/id/', methods=['POST'])
def api_create_short_link():
    data = request.get_json(silent=True)
    try:
        if data is None:
            raise EmptyError(EMPTY_REQUEST_BODY)
        original = data.get(ORIGINAL_URL_KEY)
        if original is None:
            raise EmptyError(NO_URL)
        link_validator(
            link=original,
            pattern=ORIGINAL_URL_PATTERN,
            max_length=ORIGINAL_URL_MAX_LENGTH,
            message=WRONG_ORIGINAL_URL
        )
        new_short = data.get(SHORT_LINK_KEY)
        if new_short:
            link_validator(
                link=new_short,
                pattern=SHORT_LINK_PATTERN,
                max_length=SHORT_LINK_MAX_LENGTH,
                message=WRONG_SHORT_URL
            )
            if get_records(URLMap, short=new_short):
                raise ValidationError(DUPLICATE_SHORT_LINK)
        else:
            exists_short = get_exists_short_for_original(original=original)
            if not exists_short:
                new_short = get_unique_short_id()
        if new_short:
            write_to_databese(db, URLMap, short=new_short, original=original)
    except (EmptyError, ValidationError) as error:
        raise APIException(str(error), HTTPStatus.BAD_REQUEST)
    except DataBaseError as error:
        raise APIException(str(error), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        raise APIException(SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR)
    return (
        jsonify(dict(
            url=original,
            short_link=url_for(
                'redirect_view',
                short=(new_short or exists_short),
                _external=True
            )
        )),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    records = get_records(URLMap, short=short_id)
    if not records:
        raise APIException(SHORT_LINK_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(dict(url=records[0].original)),  HTTPStatus.OK
