# Generated by Django 4.1.5 on 2023-03-31 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canasta', '0009_rename_sells_sell'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='format',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]