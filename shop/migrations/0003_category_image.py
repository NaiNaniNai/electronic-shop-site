# Generated by Django 5.0.3 on 2024-03-23 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="category/", verbose_name="Фотография"
            ),
        ),
    ]
