# Generated by Django 5.1.4 on 2025-01-10 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internet_shop_app', '0003_alter_productcategory_options_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
