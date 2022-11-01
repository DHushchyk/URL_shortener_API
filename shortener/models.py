from django.db import models
from django.utils import timezone

from shortener.utils import create_shortened_url


class Shortener(models.Model):
    original_url = models.CharField(max_length=255, unique=True)
    short_url = models.CharField(max_length=6, unique=True, blank=True)
    publishing_date = models.DateTimeField(
        default=timezone.now,
        blank=True,
    )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        if not self.short_url:
            self.short_url = create_shortened_url(self)

        super().save()

    def __str__(self):
        return f"{self.original_url} to {self.short_url}"
