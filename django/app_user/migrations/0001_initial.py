# Generated by Django 5.0.4 on 2024-11-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SirenePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyname', models.SlugField(max_length=128, unique=True, verbose_name='Permission(*)')),
                ('appname', models.SlugField(blank=True, max_length=128, null=True, verbose_name='Sirene App')),
                ('displayname', models.CharField(blank=True, max_length=500, null=True, verbose_name='Display name')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('is_builtin', models.BooleanField(default=False, verbose_name='Built-in permission')),
                ('default', models.BooleanField(default=False, verbose_name='Allowed by default')),
            ],
            options={
                'verbose_name': 'Sirene Permission',
                'verbose_name_plural': 'Sirene Permissions',
                'ordering': ['keyname'],
                'indexes': [models.Index(fields=['keyname'], name='app_user_si_keyname_0621f9_idx'), models.Index(fields=['appname'], name='app_user_si_appname_fe50a3_idx')],
            },
        ),
        migrations.CreateModel(
            name='SireneUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=128, unique=True, verbose_name='Login/Identifier(*)')),
                ('external_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='External ID')),
                ('email', models.CharField(blank=True, max_length=128, null=True, verbose_name='Email')),
                ('mobile', models.CharField(blank=True, max_length=32, null=True, verbose_name='Mobile')),
                ('firstname', models.CharField(blank=True, max_length=128, null=True, verbose_name='Firstname')),
                ('lastname', models.CharField(blank=True, max_length=128, null=True, verbose_name='Lastname')),
                ('displayname', models.CharField(blank=True, max_length=500, null=True, verbose_name='Display name')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last Login')),
                ('want_notifications', models.BooleanField(default=True, verbose_name='Want Notifications')),
                ('want_24', models.BooleanField(default=True, verbose_name='Want 24/24')),
                ('want_sms', models.BooleanField(default=False, verbose_name='Want SMS')),
                ('want_email', models.BooleanField(default=True, verbose_name='Want Email')),
                ('secondary_email', models.CharField(blank=True, max_length=128, null=True, verbose_name='Secondary Email')),
                ('secondary_mobile', models.CharField(blank=True, max_length=128, null=True, verbose_name='Secondary Mobile')),
                ('last_update', models.DateTimeField(blank=True, null=True, verbose_name='Last update')),
            ],
            options={
                'verbose_name': 'Sirene User',
                'verbose_name_plural': 'Sirene Users',
                'ordering': ['login'],
                'indexes': [models.Index(fields=['login'], name='app_user_si_login_b8ebb0_idx'), models.Index(fields=['is_enabled'], name='app_user_si_is_enab_7b9359_idx'), models.Index(fields=['displayname'], name='app_user_si_display_179714_idx'), models.Index(fields=['email'], name='app_user_si_email_878680_idx')],
            },
        ),
        migrations.CreateModel(
            name='SireneVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Username')),
                ('user_ip', models.CharField(default='', max_length=64, verbose_name='Visitor IP')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last Login')),
            ],
            options={
                'verbose_name': 'Sirene Visitor',
                'verbose_name_plural': 'Sirene Visitors',
                'ordering': ['last_login'],
                'indexes': [models.Index(fields=['username'], name='app_user_si_usernam_49437e_idx')],
            },
        ),
        migrations.CreateModel(
            name='SireneAPIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyname', models.SlugField(max_length=128, unique=True, verbose_name='Keyname')),
                ('keyvalue', models.CharField(max_length=64, verbose_name='Key value')),
                ('description', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Description')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='is_enabled')),
                ('is_readonly', models.BooleanField(default=True, verbose_name='is_readonly')),
                ('not_after', models.DateTimeField(blank=True, null=True, verbose_name='Expire after')),
                ('time_filter', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Filter Time ranges')),
                ('ip_filter', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Filter IP ranges')),
                ('acl_filter', models.TextField(blank=True, max_length=5000, verbose_name='Security ACL')),
                ('last_success', models.DateTimeField(blank=True, null=True, verbose_name='Last success')),
                ('last_error', models.DateTimeField(blank=True, null=True, verbose_name='Last error')),
                ('success_count', models.IntegerField(default=0, verbose_name='success count')),
                ('error_count', models.IntegerField(default=0, verbose_name='Error count')),
                ('last_update', models.DateTimeField(blank=True, null=True, verbose_name='Last update')),
                ('permissions', models.ManyToManyField(blank=True, to='app_user.sirenepermission')),
            ],
            options={
                'verbose_name': 'Sirene API Key',
                'verbose_name_plural': 'Sirene API Keys',
                'ordering': ['keyname'],
                'indexes': [models.Index(fields=['keyname'], name='app_user_si_keyname_42293d_idx'), models.Index(fields=['is_enabled'], name='app_user_si_is_enab_cf76d3_idx')],
            },
        ),
        migrations.CreateModel(
            name='SireneGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyname', models.SlugField(max_length=128, unique=True, verbose_name='Keyname(*)')),
                ('displayname', models.CharField(blank=True, max_length=500, null=True, verbose_name='Display name')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('is_role', models.BooleanField(default=False, verbose_name='Role')),
                ('is_builtin', models.BooleanField(default=False, verbose_name='Built-in group')),
                ('last_update', models.DateTimeField(blank=True, null=True, verbose_name='Last update')),
                ('subgroups', models.ManyToManyField(blank=True, to='app_user.sirenegroup')),
                ('permissions', models.ManyToManyField(blank=True, to='app_user.sirenepermission')),
                ('users', models.ManyToManyField(blank=True, to='app_user.sireneuser')),
            ],
            options={
                'verbose_name': 'Sirene Group',
                'verbose_name_plural': 'Sirene Groups',
                'ordering': ['keyname'],
                'indexes': [models.Index(fields=['keyname'], name='app_user_si_keyname_ed96f2_idx'), models.Index(fields=['is_enabled'], name='app_user_si_is_enab_f3d760_idx'), models.Index(fields=['is_role'], name='app_user_si_is_role_84f97c_idx')],
            },
        ),
    ]
