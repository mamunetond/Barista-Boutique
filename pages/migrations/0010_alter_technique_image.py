# Generated by Django 4.2.3 on 2023-11-07 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technique',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='development'),
        ),
    ]