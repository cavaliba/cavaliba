# Generated by Django 5.0.4 on 2024-11-16 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_home', '0002_cavalibalog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cavalibalog',
            options={'ordering': ['created'], 'verbose_name': 'Cavaliba Log', 'verbose_name_plural': 'Cavaliba Logs'},
        ),
    ]