# Generated by Django 4.1.2 on 2022-10-12 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0003_alter_gym_members_alter_member_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='members',
            field=models.ManyToManyField(blank=True, to='gym.member'),
        ),
    ]
