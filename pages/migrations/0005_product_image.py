# Generated by Django 4.2.3 on 2023-11-02 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_technique'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
