# Cricket Tales Movie Robot
# Copyright (C) 2015 Dave Griffiths
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

import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales2.settings")
import django
from django.utils import timezone
from datetime import datetime, timedelta
from crickets.models import *
import csv

import robot.exicatcher

django.setup()

# convert time from exicatcher to datetime format
def conv_time(t):
    return timezone.utc.localize(datetime(t[0],t[1],t[3],t[4],t[5],t[6],t[7]/1000))

def add_cricket(season,cricket_id,tag,gender):
    existing = Cricket.objects.filter(cricket_id=cricket_id)
    if len(existing)!=0:
        print("not adding, found cricket "+cricket_id)
        return

    print("adding cricket "+cricket_id)
    m = Cricket(cricket_id = cricket_id,
                season = season,
                tag = tag,
                gender = gender)
                
    m.save()

# need to be already split up into chunks
def add_movie(season,camera,index_filename,start_frame,fps,length_frames,start_time,end_time,cricket_id):
    name = str(season)+"-"+camera+"-"+str(start_time);

    existing = Movie.objects.filter(name=name)
    if len(existing)!=0:
        print("not adding, found movie "+name)
        return


    crickets = Cricket.objects.filter(cricket_id=cricket_id)
    if len(crickets)>0:
        print("adding movie "+name)

        index_filename = "IP"+camera+"/"+start_time.strftime('%Y%m%d')

        m = Movie(cricket = crickets[0],
                  season = season,
                  name = name,
                  created_date = timezone.now(),
                  status = 0,
                  src_index_file = index_filename,
                  start_frame = start_frame,
                  fps = fps,
                  length_frames = length_frames,
                  start_time = start_time,
                  end_time = end_time)
        m.save()
    else:
        print("add movie error, could not find cricket: "+cricket_id)

#############################################################

# returns the start/end frames for these times
def find_frames_from_index_file(exi_index_file,start_time,end_time):
    if os.path.exists(exi_index_file):
        frames = robot.exicatcher.read_index(exi_index_file)
        state = "searching"
        start = -1
        end = -1
        for num,f in enumerate(frames):
            t = conv_time(f['time'])            
            if t>start_time and state=="searching":
                start = num 
                state = "inside"
            if t>end_time and state=="inside":
                end = num
                state = "done"
        return (start,end)
    else:
        return (-1, -1)

def get_exact_frame_time(exi_frames,frame_num):
    return conv_time(exi_frames[frame_num]['time'])

data_location = "data/fake_synology/2012/"


# chop arbitrary length into videos of the same length
def add_movies(season,camera,start_time,end_time,cricket_id,video_length_secs,fps):
    exi_index_file = data_location+"IP"+camera+"/Videos/"+start_time.strftime('%Y%m%d')+".index"

    frames = find_frames_from_index_file(exi_index_file,start_time,end_time)
    start_frame = frames[0]
    end_frame = frames[1]
    total_length_frames = end_frame-start_frame

    # now we need to chop into short videos
    frames_per_video = video_length_secs*fps
    if start_frame!=-1:
        # reload the frames in so we can find out the precice times
        exi_frames = robot.exicatcher.read_index(exi_index_file)
        print("start_frame: "+str(start_frame))
        print("end_frame: "+str(end_frame))
        print("total_length_frames: "+str(total_length_frames))
        print("frames_per_video: "+str(frames_per_video))
        if total_length_frames>frames_per_video:
            for i in range(0,total_length_frames/frames_per_video):
                chop_start_frame = start_frame+i*frames_per_video
                chop_end_frame = chop_start_frame+frames_per_video
                # make sure we don't make shorter videos
                if chop_end_frame<end_frame:
                    add_movie(season,camera,exi_index_file,
                              chop_start_frame,fps,frames_per_video,
                              get_exact_frame_time(exi_frames,chop_start_frame),
                              get_exact_frame_time(exi_frames,chop_end_frame),
                              cricket_id)        


        else:
            print("not enough frames for video for cricket:"+str(cricket_id))
        
# this operates in the reverse of version 1, where the videos were 
# constructed using the source times - here we start with the crickets
# and need to go look up the videos and split them into sections
def import_crickets(filename,video_length,fps):
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                season = row[0]
                camera = row[1]
                cricket_id = row[2]
                tag = row[3]
                gender = row[4]
                start = timezone.utc.localize(datetime.strptime(row[5],"%d/%m/%Y %H:%M"))
                end = timezone.utc.localize(datetime.strptime(row[6],"%d/%m/%Y %H:%M"))

                add_cricket(season,cricket_id,tag,gender)
                add_movies(season,camera,start,end,cricket_id,video_length,fps)



import_crickets("data/VideosSingleCricketsKnownID.csv",30,10)
