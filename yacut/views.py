from http import HTTPStatus

from flask import abort, redirect, render_template

from . import app
from .exceptions import ShortGenerationError
from .forms import URLShortenerForm
from .models import URLMap


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
    except ValueError:
        return render_template('index.html', form=form)
    except ShortGenerationError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    return render_template(
        'index.html', form=form, short=url_map.get_short_url())


@app.route('/<short>')
def redirect_view(short):
    return redirect(URLMap.get_record_or_404(short=short).original)
