# Generated by Django 4.2.5 on 2023-09-13 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_location_skill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created']},
        ),
    ]
