# Generated by Django 4.1.2 on 2022-10-21 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0010_membership_level_alter_member_membership_renewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='member',
        ),
        migrations.RemoveField(
            model_name='member',
            name='membership',
        ),
    ]
