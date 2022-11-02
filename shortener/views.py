import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins


from shortener.models import Shortener
from shortener.serializers import ShortenerSerializer

from shortener.utils import create_short_url, create_short_part


class LinkViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer

    def perform_create(self, serializer):
        short_part = create_short_part()
        short_url = create_short_url(short_part, self.request)
        serializer.save(short_part=short_part, short_url=short_url)


def redirect_url_view(request, short_part):
    queryset = Shortener.objects.filter(expiration_date__gte=datetime.date.today())
    shortener = get_object_or_404(queryset, short_part=short_part)

    return HttpResponseRedirect(shortener.original_url)
