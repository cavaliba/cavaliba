# Generated by Django 5.0.4 on 2024-12-31 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_data', '0005_remove_dataclass_role_access_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datainstance',
            name='p_create',
        ),
    ]
