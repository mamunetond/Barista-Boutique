# Generated by Django 4.2.4 on 2023-11-06 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_Product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
    ]
