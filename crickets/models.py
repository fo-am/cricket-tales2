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

# for caching externally calculated values... 
class Value(models.Model):
    name = models.CharField(max_length=200)
    value = models.FloatField(default=0)
    def __unicode__(self):
        return self.name
    
class Player(models.Model):
    name = models.CharField(max_length=200)
    videos_watched = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.id)+" "+self.name

class Cricket(models.Model):
    season = models.IntegerField(default=0)
    cricket_id = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    activity = models.IntegerField(default=0)
    videos_ready = models.IntegerField(default=0)
    daynight_score = models.FloatField(default=0)
    def __unicode__(self):
        return self.tag+" "+self.cricket_id

class Movie(models.Model):
    cricket = models.ForeignKey(Cricket)
    season = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    camera = models.CharField(max_length=200)
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
        return str(self.name)+" "+str(self.camera);

class Event(models.Model):
    movie = models.ForeignKey(Movie)
    event_type = models.CharField(max_length=200)
    user = models.ForeignKey(Player, null=True, blank=True, default = None)
    video_time = models.FloatField(default=0)
    estimated_real_time = models.DateTimeField(auto_now_add=True)
    x_pos = models.FloatField(null=True, blank=True, default=None)
    y_pos = models.FloatField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    other = models.CharField(max_length=200, null=True, blank=True, default=None)
    def __unicode__(self):
        return self.event_type+" "+str(self.video_time)+" : "+str(self.movie);

    
