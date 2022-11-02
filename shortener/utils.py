from random import choice


from string import ascii_letters, digits

from django.contrib.sites.shortcuts import get_current_site

from shortener.models import Shortener

SIZE = 6

AVAILABLE_CHARS = ascii_letters + digits


def create_random_code(chars=AVAILABLE_CHARS):
    """Creates a random string with the predetermined size"""

    return "".join([choice(chars) for _ in range(SIZE)])


def create_short_part():
    """Creates a shortened part of url and checks if it is unique"""

    short_part = create_random_code()

    if Shortener.objects.filter(short_part=short_part).exists():

        return create_short_part()

    return short_part


def create_short_url(short_part, request):
    """Creates a short url"""

    current_site = get_current_site(request)

    return f"http://{current_site}/{short_part}"
