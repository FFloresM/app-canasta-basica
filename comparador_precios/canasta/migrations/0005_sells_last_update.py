# Generated by Django 4.1.5 on 2023-03-10 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canasta', '0004_remove_product_detailurl_sells_detailurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='sells',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 15, 47, 15, 772433, tzinfo=datetime.timezone.utc), verbose_name='fecha ultima busqueda'),
        ),
    ]