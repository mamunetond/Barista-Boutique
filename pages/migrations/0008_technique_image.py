# Generated by Django 4.2.3 on 2023-11-06 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='technique',
            name='image',
            field=models.ImageField(null=True, upload_to='development'),
        ),
    ]
