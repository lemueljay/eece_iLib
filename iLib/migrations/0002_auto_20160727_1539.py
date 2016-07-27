# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iLib', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('return_status', models.BooleanField(default=False)),
                ('request_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='stat',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='log',
            name='book',
            field=models.ForeignKey(to='iLib.Book'),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
