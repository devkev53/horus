# Generated by Django 4.2.6 on 2023-10-31 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_sale_discount_sale_subtotal_saledetail_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='subtotal',
        ),
    ]