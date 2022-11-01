from random import choice
from datetime import timedelta, date

from string import ascii_letters, digits

SIZE = 6

AVAILABLE_CHARS = ascii_letters + digits


def create_random_code(chars=AVAILABLE_CHARS):
    """Creates a random string with the predetermined size"""

    return "".join([choice(chars) for _ in range(SIZE)])


def create_shortened_url(model_instance):
    """Creates a shortened url and checks if it is unique"""

    shortened_part = create_random_code()
    shortened_url = f"https://sh-url/{shortened_part}"

    model_class = model_instance.__class__

    if model_class.objects.filter(short_url=shortened_url).exists():

        return create_shortened_url(model_instance)

    return shortened_url


def default_expiration_date():

    return date.today() + timedelta(days=90)
