# Generated by Django 3.2.8 on 2021-10-17 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20211016_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='primary_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images'),
        ),
    ]
