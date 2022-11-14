from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import MAX_LINK_LENGHT, REGEX_PATTERN


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message='Некорректная ссылка')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=MAX_LINK_LENGHT,
                   message=f'Длина ссылки должна быть до {MAX_LINK_LENGHT} символов'),
            Regexp(REGEX_PATTERN,
                   message='Можно использовать только латинские буквы и арабские цифры'),
            Optional()]
    )
    submit = SubmitField('Создать')
