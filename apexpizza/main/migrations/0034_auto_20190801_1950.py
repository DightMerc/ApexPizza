# Generated by Django 2.2.3 on 2019-08-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_vacancy'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pictures/')),
                ('active', models.BooleanField(default=False, verbose_name='Активен')),
                ('body', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='dinner_end',
            field=models.CharField(default='', max_length=511, verbose_name='Конец обеденного времени'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='dinner_start',
            field=models.CharField(default='', max_length=511, verbose_name='Начало обеденного времени'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='end',
            field=models.CharField(default='', max_length=511, verbose_name='Конец рабочего дня'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='start',
            field=models.CharField(default='', max_length=511, verbose_name='Начало рабочего дня'),
        ),
    ]