import re

from flask import jsonify, request, url_for

from . import app, db
from .models import URL_map
from .views import get_unique_short_id

regex_url = '^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?$'
regex_short_prefix = '[a-zA-Z0-9]+'

def to_dict(yacut):
    return dict(
        url=yacut.original,
        short_link=url_for('index_view', _external=True) + yacut.short
    )

@app.route('/api/id/<short_id>/', methods=['GET'])  
def get_original_link(short_id):
    yacut = URL_map.query.filter_by(short=short_id).first()
    if yacut is None:
        return jsonify({'message':
                        'Указанный id не найден'}), 404
    return jsonify({'url': yacut.original}), 200

@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if 'original' not in data:
        return jsonify({'message':
                        '"url" является обязательным полем!'}), 400
    if re.fullmatch(regex_url, data['original']) is None:
        return jsonify({'message':
                        'Это некорректная ссылка'}), 400
    if re.fullmatch(regex_short_prefix, data['short']) is None:
        return jsonify({'message':
                        'Указано недопустимое имя для короткой ссылки'}), 400
    yacut = URL_map()
    for field in ['original', 'short']:
        if field not in data:
            short_id = get_unique_short_id()
            setattr(yacut, field, short_id)
        else:
            setattr(yacut, field, data[field])
    db.session.add(yacut)
    db.session.commit()
    return jsonify(to_dict(yacut)), 201
