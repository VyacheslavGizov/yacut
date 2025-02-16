from flask import render_template

from . import app, db
from .models import URLMap


@app.route('/')
def index_view():
    url = URLMap(
        original='dfkfhdkjhdfkfj',
        short='dfkjhfd'
    )
    db.session.add(url)
    db.session.commit()
    return 'test string'
