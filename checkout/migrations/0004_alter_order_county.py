# Generated by Django 4.1.2 on 2022-10-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_alter_order_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='county',
            field=models.CharField(default='', max_length=40),
        ),
    ]