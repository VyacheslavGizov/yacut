from flask import redirect, render_template, flash

from . import app
from .forms import URLShortenerForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def shortener_view():
    form = URLShortenerForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create(
                short=form.custom_id.data,
                original=form.original_link.data,
                validate=False
            ).get_short_url()
        )
    except (ValueError, URLMap.ShortGenerationError) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short=short).original)
