# Generated by Django 4.2.5 on 2023-09-06 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_review_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
