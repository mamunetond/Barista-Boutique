# Generated by Django 4.2.3 on 2023-11-07 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_technique_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='development'),
        ),
    ]
