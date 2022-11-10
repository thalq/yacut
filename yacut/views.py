from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id or len(custom_id) < 1:
            custom_id = get_unique_short_id()
        yacut = URL_map(
            original=form.original_link.data,
            short=custom_id,
        )
        if URL_map.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('index.html', form=form)

        db.session.add(yacut)
        db.session.commit()
        return (render_template('index.html', form=form, short=custom_id), 200)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_link_view(short):
    original_link = URL_map.query.filter_by(short=short).first()
    if original_link is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_link.original)
