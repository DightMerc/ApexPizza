# Generated by Django 2.2.3 on 2019-07-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_remove_priceforsize_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceforsize',
            name='price',
            field=models.FloatField(default=0, verbose_name='Цена'),
        ),
    ]
