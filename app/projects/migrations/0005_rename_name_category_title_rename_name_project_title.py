# Generated by Django 4.2.6 on 2024-01-04 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='name',
            new_name='title',
        ),
    ]