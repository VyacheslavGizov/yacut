import re
from flask import request, jsonify, url_for
from http import HTTPStatus

from . import app, db
from .error_handlers import APIExceptions
from .utils import regex_validation, get_records, get_unique_short_id, write_to_databese
from .models import URLMap
from .views import get_exists_short_for_original, get_records

URL_PATTERN = re.compile(
    r'^[a-z]+://[^\/\?:]+([0-9]+)?(\/.*?)?(\?.*)?$', re.IGNORECASE)
SHORT_PATTERN = r'^[a-zA-Z0-9]+$'
MAX_LENGTH = 16


@app.route('/api/id/', methods=['POST'])
def api_create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise APIExceptions('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    original = data.get('url')
    if original is None:
        raise APIExceptions('"url" является обязательным полем!')
    regex_validation(URL_PATTERN, original, 'Недопустимый формат для ссылки.')  # длинную ссылку тоже надо на длину проверить
    short = data.get('custom_id')
    if short is not None:
        if len(short) > MAX_LENGTH:
            raise APIExceptions('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
        regex_validation(SHORT_PATTERN, short, 'Указано недопустимое имя для короткой ссылки')
        if get_records(URLMap, short=short):
            raise APIExceptions('Предложенный вариант короткой ссылки уже существует.', HTTPStatus.BAD_REQUEST)
    else:
        exists_short = get_exists_short_for_original(original=original)
        if not exists_short:
            short = get_unique_short_id()
    if short:
        try:
            write_to_databese(
                db, URLMap, short=short, original=original)
        except Exception:
            raise APIExceptions('Ошибка сервера.', HTTPStatus.INTERNAL_SERVER_ERROR)
    short = short or exists_short
    return (jsonify(dict(url=original, short_link=url_for(
        'redirect_view', short=short, _external=True))), 201)


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    records = get_records(URLMap, short=short_id)
    if not records:
        raise APIExceptions(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify(dict(url=records[0].original)),  HTTPStatus.OK
