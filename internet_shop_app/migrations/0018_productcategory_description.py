# Generated by Django 4.2.18 on 2025-01-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internet_shop_app', '0017_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
