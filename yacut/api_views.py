import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id
from settings import MAX_LINK_LENGHT, REGEX_PATTERN, URL_REGEX_PATTERN


def to_dict(yacut):
    return dict(
        url=yacut.original,
        short_link=url_for('index_view', _external=True) + yacut.short
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    yacut = URL_map.query.filter_by(short=short_id).first()
    if yacut is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': yacut.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    print(data)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original = data.get('url')
    if not original:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if re.fullmatch(URL_REGEX_PATTERN, original) is None:
        raise InvalidAPIUsage('Это некорректная ссылка')
    if (
        'custom_id' in data and data['custom_id'] is not None and
        len(data['custom_id']) > 0
    ):
        short = data['custom_id']
        if (
            len(short) > MAX_LINK_LENGHT or
            not re.fullmatch(REGEX_PATTERN, short)
        ):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        elif URL_map.query.filter_by(short=short).first():
            raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
    else:
        short = get_unique_short_id()

    yacut = URL_map(
        original=original,
        short=short
    )
    db.session.add(yacut)
    db.session.commit()
    return jsonify(to_dict(yacut)), HTTPStatus.CREATED
