from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import APIException
from .exceptions import ShortGenerationError
from .models import URLMap


EMPTY_REQUEST_BODY = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
SHORT_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise APIException(EMPTY_REQUEST_BODY)
    original = data.get('url')
    if original is None:
        raise APIException(NO_URL)
    short = data.get('custom_id')
    try:
        url_map = URLMap.create(short=short, original=original)
    except ValueError as error:
        raise APIException(str(error), HTTPStatus.BAD_REQUEST)
    except ShortGenerationError as error:
        raise APIException(str(error), HTTPStatus.INTERNAL_SERVER_ERROR)
    return (
        jsonify(dict(url=original, short_link=url_map.get_short_url())),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get_record(short=short_id)
    if not url_map:
        raise APIException(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(dict(url=url_map.original)), HTTPStatus.OK
