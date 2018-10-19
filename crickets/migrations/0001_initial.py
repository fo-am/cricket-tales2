# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cricket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eating_score', models.IntegerField(default=0)),
                ('singing_score', models.IntegerField(default=0)),
                ('moving_score', models.IntegerField(default=0)),
                ('daynight_score', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.FloatField(default=0)),
                ('end_time', models.FloatField(default=0)),
                ('x_pos', models.FloatField(default=None, null=True, blank=True)),
                ('y_pos', models.FloatField(default=None, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('other', models.CharField(default=None, max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('es_name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('views', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(verbose_name=b'date created')),
                ('status', models.IntegerField(default=0)),
                ('src_index_file', models.CharField(max_length=4096)),
                ('start_frame', models.IntegerField(default=0)),
                ('fps', models.FloatField(default=0)),
                ('length_frames', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(verbose_name=b'start time')),
                ('end_time', models.DateTimeField(verbose_name=b'end time')),
                ('num_events', models.IntegerField(default=0)),
                ('cricket', models.ForeignKey(to='crickets.Cricket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unique_id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('videos_watched', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='movie',
            field=models.ForeignKey(to='crickets.Movie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ForeignKey(to='crickets.EventType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to='crickets.Player', null=True),
            preserve_default=True,
        ),
    ]
