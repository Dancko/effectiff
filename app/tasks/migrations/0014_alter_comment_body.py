# Generated by Django 4.2.6 on 2023-11-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_alter_commentfile_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
