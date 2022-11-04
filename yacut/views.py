import random
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URL_map

def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_prefix = ''.join(random.sample(letters_and_digits, 6))
    url_start_with = 'http://yacut/'
    short_url = url_start_with+ short_prefix
    return  short_url

@app.route('/', methods=['GET', 'POST'])
def index_view():
    form =URLForm()
    if form.validate_on_submit():
        short=form.short.data
        if not short:
            short = get_unique_short_id()
        yacut = URL_map(
            original=form.original.data,
            short=form.short.data,
        )
        db.session.add(yacut)
        db.session.commit()
    return render_template('index.html', form=form)
