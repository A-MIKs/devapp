# Generated by Django 4.2.5 on 2023-09-13 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
