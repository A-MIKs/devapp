# Generated by Django 4.2.5 on 2023-09-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_vote_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]