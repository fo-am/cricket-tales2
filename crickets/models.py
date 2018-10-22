# Cricket Tales V2
# Copyright (C) 2018 FoAM Kernow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from datetime import datetime

class Player(models.Model):
    unique_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    videos_watched = models.IntegerField(default=0)

class Cricket(models.Model):
    season = models.IntegerField(default=0)
    cricket_id = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    eating_score = models.IntegerField(default=0)
    singing_score = models.IntegerField(default=0)
    moving_score = models.IntegerField(default=0)
    daynight_score = models.IntegerField(default=0)
    def __unicode__(self):
        return self.tag+" "+self.cricket_id

class Movie(models.Model):
    cricket = models.ForeignKey(Cricket)
    season = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField('date created')
    status = models.IntegerField(default=0)
    src_index_file = models.CharField(max_length=4096)
    start_frame = models.IntegerField(default=0)
    fps = models.FloatField(default=0)
    length_frames = models.IntegerField(default=0)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    # stuff updated from periodic update.py
    num_events = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.name);

class EventType(models.Model):
    name = models.CharField(max_length=200)
    es_name = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.name);

class Event(models.Model):
    movie = models.ForeignKey(Movie)
    type = models.ForeignKey(EventType)
    user = models.ForeignKey(Player, null=True, blank=True, default = None)
    start_time = models.FloatField(default=0)
    end_time = models.FloatField(default=0)
    x_pos = models.FloatField(null=True, blank=True, default=None)
    y_pos = models.FloatField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    other = models.CharField(max_length=200, null=True, blank=True, default=None)
    def __unicode__(self):
        return self.type.name+" "+str(self.start_time)+" : "+str(self.movie);

    
