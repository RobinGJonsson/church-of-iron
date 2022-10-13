# Generated by Django 4.1.2 on 2022-10-13 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('gym', '0004_alter_gym_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='price',
            new_name='month_price',
        ),
        migrations.RemoveField(
            model_name='member',
            name='address',
        ),
        migrations.RemoveField(
            model_name='member',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='phone',
        ),
        migrations.AddField(
            model_name='member',
            name='member_since',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='membership_renewed',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='payment_plan',
            field=models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile'),
        ),
    ]
