from flask import flash, redirect, render_template

from . import app
from .exceptions import ValidationError
from .forms import URLShortenerForm
from .models import URLMap


DUPLICATE_SHORT_LINK = 'Предложенный вариант короткой ссылки уже существует.'
LINK_IS_DONE = 'Ваша новая ссылка готова:'
WRONG_DATA = 'wrong_input'
DONE = 'link_is_done'


@app.route('/', methods=['GET', 'POST'])
def shortener_view():
    form = URLShortenerForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            short=form.custom_id.data,
            original=form.original_link.data
        )
    except ValidationError as error:
        flash(str(error))
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        short=url_map.get_short_url()
    )


@app.route('/<short>')
def redirect_view(short):
    return redirect(URLMap.get_record_or_404(short=short).original)
