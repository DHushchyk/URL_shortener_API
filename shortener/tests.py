import datetime
from urllib.parse import urljoin

from unittest import mock
from django.test import TestCase
from rest_framework.test import APIClient

from rest_framework import status

from shortener.models import Shortener
from shortener.serializers import ShortenerSerializer

BASE_URL = "http://127.0.0.1:8000/"
LINKS_URL = urljoin(BASE_URL, "api/links/")
ORIGINAL_URL_SAMPLE = "https://www.django-rest-framework.org/"


def create_sample_link(client, url=ORIGINAL_URL_SAMPLE, expiration_date=""):
    payload = {"original_url": url, "expiration_date": expiration_date}

    return client.post(LINKS_URL, payload)


def get_detail_url(link):
    link_id = link.data["id"]
    return f"{LINKS_URL}{link_id}/"


class ShortenerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_link_without_expiration_date(self):
        res = create_sample_link(self.client)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_link_with_correct_expiration_date(self):
        res = create_sample_link(
            self.client, expiration_date=datetime.date(2023, 1, 31)
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @mock.patch("shortener.models.datetime", wraps=datetime)
    def test_create_link_with_wrong_expiration_date(self, mock_datetime):
        mock_datetime.date.today.return_value = datetime.date(2022, 11, 11)
        res_first_date = create_sample_link(
            self.client, expiration_date=datetime.date(2022, 10, 11)
        )
        res_second_date = create_sample_link(
            self.client, expiration_date=datetime.date(2023, 11, 12)
        )

        self.assertEqual(
            res_first_date.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res_second_date.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_link_list(self):
        create_sample_link(self.client)
        create_sample_link(self.client, url="https://github.com/")
        create_sample_link(self.client, url="https://www.flashscore.ua")
        res = self.client.get(LINKS_URL)

        links = Shortener.objects.all()
        serializer = ShortenerSerializer(links, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_link_detail(self):
        link = create_sample_link(self.client)
        res = self.client.get(get_detail_url(link))

        link_from_db = Shortener.objects.get(id=link.data["id"])
        serializer = ShortenerSerializer(link_from_db)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_redirect_short_link(self):
        link = create_sample_link(self.client)
        redirect_link = link.data["short_url"]
        res = self.client.get(redirect_link)

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

    @mock.patch("shortener.views.datetime", wraps=datetime)
    def test_redirect_expired_short_link(self, mock_datetime):
        mock_datetime.date.today.return_value = datetime.date(2023, 1, 2)
        link = create_sample_link(
            self.client, expiration_date=datetime.date(2023, 1, 1)
        )
        redirect_link = link.data["short_url"]
        res = self.client.get(redirect_link)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
