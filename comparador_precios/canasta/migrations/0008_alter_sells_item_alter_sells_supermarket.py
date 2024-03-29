# Generated by Django 4.1.5 on 2023-03-31 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('canasta', '0007_brand_alter_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sells',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canasta.product'),
        ),
        migrations.AlterField(
            model_name='sells',
            name='supermarket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canasta.supermarket'),
        ),
    ]
