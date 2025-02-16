from flask import render_template, flash

from . import app, db
from .models import URLMap
from .forms import URLShortenerForm
from .utils import get_random_string, record_exists


EXISTS_MESSAGE = 'Такая короткая ссылка была добавлена ранее!'


@app.route('/', methods=['GET', 'POST'])
def shortener_view():  # возможно переименовать
    form = URLShortenerForm()
    if form.validate_on_submit():
        short = form.short.data
        if not short:
            short = get_random_string()
            # добавить счетчик в цикл и выбросить исключение и прервать цикл
            while record_exists(URLMap, short=short):
                short = get_random_string()
        elif record_exists(URLMap, short=short):
            flash(EXISTS_MESSAGE, 'exist')
            return render_template('shortener.html', form=form)
        url_map = URLMap(
            original=form.original.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
    return render_template('shortener.html', form=form)
