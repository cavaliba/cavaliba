# Generated by Django 5.0.4 on 2025-01-25 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_data', '0009_datalink_label2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datalink',
            name='label1',
        ),
        migrations.RemoveField(
            model_name='datalink',
            name='label2',
        ),
    ]
