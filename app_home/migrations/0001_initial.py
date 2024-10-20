# Generated by Django 5.0.4 on 2024-07-20 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyname', models.SlugField(max_length=100, unique=True, verbose_name='Key name(*)')),
                ('displayname', models.CharField(blank=True, max_length=128, verbose_name='Display name')),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('url', models.CharField(blank=True, default='', max_length=1500, verbose_name='URL')),
                ('icon', models.CharField(blank=True, default='', max_length=128, verbose_name='Icon')),
                ('page', models.CharField(blank=True, default='', max_length=128, verbose_name='Page')),
                ('order', models.IntegerField(default=100, verbose_name='Order')),
                ('state', models.CharField(choices=[('enabled', 'enabled'), ('disabled', 'disabled'), ('hidden', 'hidden')], default='enabled', max_length=20, verbose_name='State')),
                ('version', models.CharField(blank=True, default='', max_length=128, verbose_name='Version')),
                ('permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_user.sirenepermission')),
            ],
            options={
                'verbose_name': 'Dashboard Application',
                'verbose_name_plural': 'Dashboard Applications',
                'db_table': 'app_home_dashboard_app',
                'ordering': ['order'],
            },
        ),
    ]
