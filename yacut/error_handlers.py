from http import HTTPStatus

from flask import jsonify, render_template

from . import app
from .exceptions import APIException


@app.errorhandler(APIException)
def api_exceptions(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
