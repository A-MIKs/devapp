# Generated by Django 4.2.5 on 2023-09-05 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_product_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='vote_totlal',
            new_name='vote_total',
        ),
    ]
