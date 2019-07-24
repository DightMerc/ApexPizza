# Generated by Django 2.2.3 on 2019-07-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190721_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='PizzaUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=511, verbose_name='Название')),
                ('active', models.BooleanField(default=False)),
                ('cashback', models.PositiveIntegerField()),
            ],
        ),
    ]