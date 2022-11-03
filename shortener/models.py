import datetime

from django.db import models
from rest_framework.exceptions import ValidationError

MIN_EXP_DATE = datetime.date.today() + datetime.timedelta(days=1)
MAX_EXP_DATE = datetime.date.today() + datetime.timedelta(days=365)


def default_expiration_date():
    return datetime.date.today() + datetime.timedelta(days=90)


class Shortener(models.Model):
    original_url = models.CharField(max_length=255, unique=True)
    short_part = models.CharField(max_length=6, unique=True, blank=True)
    short_url = models.CharField(max_length=255, unique=True, blank=True)
    publishing_date = models.DateField(auto_now=True)
    expiration_date = models.DateField(default=default_expiration_date)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Shortened link'
        verbose_name_plural = 'Shortened links'

    def __str__(self):
        return f"{self.id}: {self.original_url}"

    def clean(self):
        if not MIN_EXP_DATE <= self.expiration_date < MAX_EXP_DATE:
            raise ValidationError(
                {
                    "expiration_date": f"date must be in range "
                    f"{str(MIN_EXP_DATE)}-"
                    f"{MAX_EXP_DATE}."
                }
            )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()
        return super(Shortener, self).save(
            force_insert, force_update, using, update_fields
        )
