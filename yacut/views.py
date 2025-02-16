from flask import render_template

from . import app, db
from .models import URLMap
from .forms import URLShortenerForm


@app.route('/', methods=['GET', 'POST'])
def shortener_view():  # возможно переименовать
    form = URLShortenerForm()
    if form.validate_on_submit():
        url_map = URLMap(
            original=form.original.data,
            short=form.short.data
        )
        db.session.add(url_map)
        db.session.commit()
    return render_template('shortener.html', form=form)
