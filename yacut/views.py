from flask import render_template, flash, redirect, abort

from . import app, db
from .models import URLMap
from .forms import URLShortenerForm
from .utils import get_unique_short_id, get_records, write_to_databese


EXISTS_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
LINK_MESSAGE = 'Ваша новая ссылка готова:'
WRONG_DATA = 'wrong_input'
LINK_IS_DONE = 'link_is_done'


def get_exists_short_for_original(original, length=6):
    for short in (record.short for record in
                  get_records(URLMap, original=original)):
        if len(short) == length:
            return short


@app.route('/', methods=['GET', 'POST'])
def shortener_view():
    form = URLShortenerForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short and get_records(URLMap, short=short):
            flash(EXISTS_MESSAGE, WRONG_DATA)
            return render_template('shortener.html', form=form)
        if not short:
            exists_short = get_exists_short_for_original(
                original=form.original_link.data)
            if not exists_short:
                short = get_unique_short_id()
        if short:
            try:
                write_to_databese(
                    db, URLMap, short=short, original=form.original_link.data)
            except Exception:
                abort(500)
        short = short or exists_short
        flash(LINK_MESSAGE, LINK_IS_DONE)
        return render_template('shortener.html', form=form, short=short)
    return render_template('shortener.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
