# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, blank=True)),
                ('code', models.CharField(unique=True, max_length=40)),
                ('expired_at', models.DateTimeField(null=True, blank=True)),
                ('redirect_to', models.CharField(max_length=512)),
                ('target_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('target_content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True, on_delete=models.SET_NULL)),
                ('user', models.ForeignKey(related_name='referral_codes', to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferralResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_key', models.CharField(max_length=40)),
                ('ip_address', models.CharField(max_length=45)),
                ('action', models.CharField(max_length=128)),
                ('target_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('referral', models.ForeignKey(related_name='responses', to='referrals.Referral', on_delete=models.CASCADE)),
                ('target_content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True, on_delete=models.SET_NULL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
