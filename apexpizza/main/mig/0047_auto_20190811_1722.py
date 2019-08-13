# Generated by Django 2.2.3 on 2019-08-11 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_auto_20190811_1711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_created_date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_created_drinks',
            new_name='drinks',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_pizzas',
            new_name='pizzas',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_presents',
            new_name='presents',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_sauces',
            new_name='sauces',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_sets',
            new_name='sets',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_snacks',
            new_name='snacks',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_state',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='archievedorder',
            old_name='archieve_order_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='archievedorder',
            name='archieve_order_active',
        ),
        migrations.RemoveField(
            model_name='archievedorder',
            name='archieve_order_address',
        ),
        migrations.RemoveField(
            model_name='archievedorder',
            name='archieve_order_id',
        ),
        migrations.RemoveField(
            model_name='archievedorder',
            name='archieve_order_info',
        ),
        migrations.RemoveField(
            model_name='archievedorder',
            name='archieve_order_user',
        ),
        migrations.AddField(
            model_name='archievedorder',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Актуально'),
        ),
        migrations.AddField(
            model_name='archievedorder',
            name='address',
            field=models.TextField(default='', verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='archievedorder',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='archievedorder',
            name='info',
            field=models.TextField(default='', verbose_name='Инфо'),
        ),
        migrations.AddField(
            model_name='archievedorder',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.User'),
        ),
    ]
