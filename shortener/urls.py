from django.urls import path, include
from rest_framework import routers

from shortener.views import LinkViewSet, redirect_url_view

router = routers.DefaultRouter()
router.register("links", LinkViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("<str:short_part>/", redirect_url_view, name="redirect"),
]

app_name = "shortener"
