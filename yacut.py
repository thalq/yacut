import random
import string
from datetime import datetime

from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional

app = Flask(__name__, template_folder='html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку, которую будем укорачивать.',
        validators=[DataRequired(message='Обязательное поле'),Length(1, 256)]
    )
    custom_id = StringField(
        'Введите вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать') 

class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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

if __name__ == '__main__':
    app.run()
