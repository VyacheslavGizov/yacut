import random
import string


def get_random_string(length=6, alpfabet=None):
    alpfabet = (string.ascii_letters + string.digits
                if alpfabet is None
                else alpfabet)
    return ''.join(random.choice(alpfabet) for _ in range(length))


def record_exists(model, **fields):
    return model.query.filter_by(**fields).first() is not None
