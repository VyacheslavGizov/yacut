from flask import render_template, flash, redirect

from . import app, db
from .models import URLMap
from .forms import URLShortenerForm
from .utils import get_random_string, record_exists


EXISTS_MESSAGE = 'Такая короткая ссылка была добавлена ранее!'
LINK_MESSAGE = 'Ваша новая ссылка готова:'
WRONG_DATA = 'wrong_input'
LINK_IS_DONE = 'link_is_done'


@app.route('/', methods=['GET', 'POST'])
def shortener_view():
    form = URLShortenerForm()
    if form.validate_on_submit():
        short = form.short.data
        if short and record_exists(URLMap, short=short):
            flash(EXISTS_MESSAGE, WRONG_DATA)
            return render_template('shortener.html', form=form)
        if not short:
            short = get_random_string()
            # добавить счетчик в цикл и выбросить исключение и прервать цикл
            while record_exists(URLMap, short=short):
                short = get_random_string()
        url_map = URLMap(
            original=form.original.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        flash(LINK_MESSAGE, LINK_IS_DONE)
        return render_template('shortener.html', form=form, short=short)
    return render_template('shortener.html', form=form)


@app.route('/<short>/')
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)
