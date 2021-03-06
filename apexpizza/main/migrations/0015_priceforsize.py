# Generated by Django 2.2.3 on 2019-07-24 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20190724_2345'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceForSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=511, verbose_name='Название')),
                ('pizza', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Pizza')),
                ('size', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='main.Size')),
            ],
        ),
    ]
