# Generated by Django 3.2.3 on 2023-06-25 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230624_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': '\u200bПодписки'},
        ),
    ]
