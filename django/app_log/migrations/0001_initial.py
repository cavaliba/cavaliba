# Generated by Django 5.0.4 on 2024-11-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SireneLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(blank=True, default='', max_length=200, verbose_name='App')),
                ('view', models.CharField(blank=True, default='', max_length=200, verbose_name='View')),
                ('action', models.CharField(blank=True, default='', max_length=200, verbose_name='Action')),
                ('status', models.CharField(blank=True, default='', max_length=32, verbose_name='Status')),
                ('data', models.CharField(default='', max_length=2000, verbose_name='data')),
                ('level', models.CharField(default='na', max_length=20, verbose_name='Level')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('username', models.CharField(default='na', max_length=256, verbose_name='Username')),
                ('user_ip', models.CharField(default='', max_length=64, verbose_name='User IP')),
            ],
            options={
                'verbose_name': 'Sirene Log',
                'verbose_name_plural': 'Sirene Logs',
                'ordering': ['created'],
            },
        ),
    ]
