# Generated by Django 4.1.2 on 2022-10-19 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_alter_order_street_address2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='original_bag',
            new_name='original_cart',
        ),
    ]