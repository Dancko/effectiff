# Generated by Django 4.2.4 on 2023-08-02 11:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_user_teammates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]