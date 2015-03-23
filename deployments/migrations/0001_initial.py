# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseChecklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version_number', models.CharField(max_length=12)),
                ('build_number', models.CharField(max_length=8, null=True, blank=True)),
                ('platform', models.CharField(max_length=20, choices=[(b'Android', b'Android'), (b'iOS', b'iOS')])),
                ('release_date', models.DateField(null=True, blank=True)),
                ('commit_sha', models.CharField(max_length=256, null=True, blank=True)),
                ('uses_prod', models.BooleanField(default=False, verbose_name=b'Uses production settings')),
                ('secure_http', models.BooleanField(default=False, verbose_name=b'Verify https and MITM security')),
                ('push_notify', models.BooleanField(default=False, verbose_name=b'Verify push notifications, including aps-environment value')),
                ('ssl_cert_valid', models.BooleanField(default=False, verbose_name=b'Verify SSL validity')),
                ('bad_email_check', models.BooleanField(default=False, verbose_name=b'Handles bad email error')),
                ('bad_domain_check', models.BooleanField(default=False, verbose_name=b'Handles bad domain error')),
                ('bad_auth_check', models.BooleanField(default=False, verbose_name=b'Handles permission denied error')),
                ('released_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
