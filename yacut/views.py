import random
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URL_map


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_prefix = ''.join(random.sample(letters_and_digits, 6))
    return short_prefix

@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id=form.custom_id.data
        if URL_map.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
        if not custom_id:
            custom_id = get_unique_short_id()
        yacut = URL_map(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(yacut)
        db.session.commit()
        return (render_template('index.html', form=form, short=custom_id), 200)
    return render_template('index.html', form=form)

@app.route('/<string:short>')
def short_link_view(short):
    original_link = URL_map.query.filter_by(short=short).first().original
    return redirect(original_link)
