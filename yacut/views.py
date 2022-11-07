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
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id=form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    yacut = URL_map(
        original=form.original_link.data,
        short=custom_id,
    )
    db.session.add(yacut)
    db.session.commit()
    flash(url_for('short_link_view', short=custom_id, _external=True), "link")
    return render_template('index.html', form=form)

@app.route('/<string:short>')
def short_link_view(short):
    original_link = URL_map.query.filter_by(short=short).first().original
    return redirect(original_link)
