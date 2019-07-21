# Generated by Django 2.2.3 on 2019-07-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='doughType',
        ),
        migrations.AddField(
            model_name='pizza',
            name='doughType',
            field=models.ManyToManyField(to='main.DoughType'),
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='size',
        ),
        migrations.AddField(
            model_name='pizza',
            name='size',
            field=models.ManyToManyField(to='main.Size'),
        ),
    ]
