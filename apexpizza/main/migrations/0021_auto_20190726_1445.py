# Generated by Django 2.2.3 on 2019-07-26 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20190725_0135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='drinks',
        ),
        migrations.RemoveField(
            model_name='set',
            name='pizzas',
        ),
        migrations.RemoveField(
            model_name='set',
            name='sauces',
        ),
        migrations.RemoveField(
            model_name='set',
            name='snacks',
        ),
    ]
