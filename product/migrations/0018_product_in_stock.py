# Generated by Django 3.2.8 on 2021-10-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_alter_product_primary_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.IntegerField(default=0),
        ),
    ]
