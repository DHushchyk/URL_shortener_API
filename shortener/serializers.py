from rest_framework import serializers

from shortener.models import Shortener


class ShortenerSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)
    publishing_date = serializers.DateField(read_only=True)

    class Meta:
        model = Shortener
        fields = [
            "id",
            "original_url",
            "short_url",
            "publishing_date",
            "expiration_date",
        ]
