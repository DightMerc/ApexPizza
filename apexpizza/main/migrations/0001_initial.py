# Generated by Django 2.2.3 on 2019-07-20 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoughType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=511, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=511, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=511, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pictures/')),
                ('title', models.CharField(default='', max_length=511, verbose_name='Название')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('doughType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Теста', to='main.DoughType')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Размер', to='main.Size')),
                ('toppings', models.ManyToManyField(to='main.Topping')),
            ],
        ),
    ]
