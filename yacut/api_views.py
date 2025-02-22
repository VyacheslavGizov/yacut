from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import APIException
from .models import URLMap


EMPTY_REQUEST_BODY = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
SHORT_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise APIException(EMPTY_REQUEST_BODY)
    if 'url' not in data:
        raise APIException(NO_URL)
    original = data['url']
    try:
        return (
            jsonify(dict(
                url=original,
                short_link=URLMap.create(
                    short=data.get('custom_id'),
                    original=original).get_short_url()
            )),
            HTTPStatus.CREATED
        )
    except ValueError as error:
        raise APIException(str(error))
    except URLMap.ShortGenerationError as error:
        raise APIException(str(error), HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/api/id/<short>/')
def get_original_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise APIException(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(dict(url=url_map.original)), HTTPStatus.OK
