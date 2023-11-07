# Generated by Django 4.2.4 on 2023-11-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('keyword', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('description', models.CharField(max_length=1200)),
                ('created_at_product', models.DateTimeField(auto_now=True)),
                ('updated_at_product', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(blank=True)),
            ],
        ),
    ]
