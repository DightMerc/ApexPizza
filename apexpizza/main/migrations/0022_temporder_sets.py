# Generated by Django 2.2.3 on 2019-07-26 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20190726_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporder',
            name='sets',
            field=models.ManyToManyField(to='main.Set'),
        ),
    ]