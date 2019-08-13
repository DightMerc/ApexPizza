# Generated by Django 2.2.3 on 2019-07-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20190729_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Present',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pictures/')),
                ('title', models.CharField(default='', max_length=511, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='TempPresent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pictures/')),
                ('title', models.CharField(default='', max_length=511, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='temporder',
            name='presents',
            field=models.ManyToManyField(to='main.TempPresent'),
        ),
    ]