# Generated by Django 2.2.3 on 2019-08-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_auto_20190801_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='show_body',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=models.TextField(default=''),
        ),
    ]
