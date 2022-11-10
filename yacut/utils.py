import random
import string

from .models import URL_map


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_prefix = ''.join(random.sample(letters_and_digits, 6))
    if URL_map.query.filter_by(short=short_prefix).first():
        return get_unique_short_id()
    return short_prefix
