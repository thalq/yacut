from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку, которую будем укорачивать.',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(require_tld=True, message='Некорректная ссылка')
        ]
    )
    custom_id = StringField(
        'Введите вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать') 
