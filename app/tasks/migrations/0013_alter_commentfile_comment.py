# Generated by Django 4.2.6 on 2023-11-19 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_commentfile_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfile',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='tasks.comment'),
        ),
    ]
