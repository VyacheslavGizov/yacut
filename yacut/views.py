from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .exceptions import DataBaseError
from .forms import URLShortenerForm
from .models import URLMap
from .utils import get_records, get_unique_short_id, write_to_databese


DUPLICATE_SHORT_LINK = 'Предложенный вариант короткой ссылки уже существует.'
LINK_IS_DONE = 'Ваша новая ссылка готова:'
WRONG_DATA = 'wrong_input'
DONE = 'link_is_done'


@app.route('/', methods=['GET', 'POST'])
def shortener_view():
    form = URLShortenerForm()
    if form.validate_on_submit():
        new_short = form.custom_id.data
        if new_short and get_records(URLMap, short=new_short):
            flash(DUPLICATE_SHORT_LINK)
            return render_template('shortener.html', form=form)
        if not new_short:
            new_short = get_unique_short_id()
        try:
            write_to_databese(db, URLMap, short=new_short,
                              original=form.original_link.data)
        except DataBaseError:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        flash(LINK_IS_DONE, DONE)
        return render_template(
            'shortener.html',
            form=form,
            short=new_short
        )
    return render_template('shortener.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
