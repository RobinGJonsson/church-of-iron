# Generated by Django 4.1.2 on 2022-11-12 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0014_membership_activation_fee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymSImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('alt', models.CharField(max_length=50)),
                ('gym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
            ],
        ),
    ]
