# Generated by Django 4.1.3 on 2022-11-03 16:56

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0003_alter_shortener_expiration_date_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shortener",
            options={
                "ordering": ["id"],
                "verbose_name": "Shortened link",
                "verbose_name_plural": "Shortened links",
            },
        ),
        migrations.AlterField(
            model_name="shortener",
            name="expiration_date",
            field=models.DateField(default=shortener.models.default_expiration_date),
        ),
    ]