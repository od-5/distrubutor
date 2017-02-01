# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('coord_x', models.DecimalField(null=True, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430', max_digits=9, decimal_places=6, blank=True)),
                ('coord_y', models.DecimalField(null=True, verbose_name='\u0414\u043e\u043b\u0433\u043e\u0442\u0430', max_digits=9, decimal_places=6, blank=True)),
                ('timezone', models.SmallIntegerField(default=0, verbose_name='\u0427\u0430\u0441\u043e\u0432\u043e\u0439 \u043f\u043e\u044f\u0441', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])),
            ],
            options={
                'verbose_name': '\u0413\u043e\u0440\u043e\u0434',
                'verbose_name_plural': '\u0413\u043e\u0440\u043e\u0434\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('code', models.CharField(max_length=10, verbose_name='\u041a\u043e\u0434')),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', blank=True, to='geolocation.Country', null=True),
            preserve_default=True,
        ),
    ]
