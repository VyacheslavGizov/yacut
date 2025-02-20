from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import APIException
from .exceptions import ValidationError, ShortGenerationError
from .models import URLMap


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
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise APIException(EMPTY_REQUEST_BODY)
    original = data.get(ORIGINAL_URL_KEY)
    if original is None:
        raise APIException(NO_URL)
    short = data.get(SHORT_LINK_KEY)
    try:
        url_map = URLMap.create(short=short, original=original)
    except ValidationError as error:
        raise APIException(str(error), HTTPStatus.BAD_REQUEST)
    except ShortGenerationError as error:
        raise APIException(str(error), HTTPStatus.INTERNAL_SERVER_ERROR)
    return (
        jsonify(dict(url=original, short_link=url_map.get_short_url())),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get_record_by_fields(short=short_id)
    if not url_map:
        raise APIException(SHORT_LINK_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(dict(url=url_map.original)), HTTPStatus.OK
