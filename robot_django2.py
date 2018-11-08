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
from django.db.models import Max, Count, Sum, Q
from datetime import datetime, timedelta, date, time
from crickets.models import *
import csv
import time
import subprocess
import numpy as np
import robot.exicatcher
import robot.process
import robot.settings
import robot.plot
import crickets.common
import random

django.setup()

# convert time from exicatcher to datetime format
def conv_time(t):
    return timezone.utc.localize(datetime(t[0],t[1],t[3],t[4],t[5],t[6],t[7]/1000))

def trunc_time(t):
    return timezone.utc.localize(datetime(t.year,t.month,t.day,0,0,0,0))

#######################################################################
# a note on movie status flag:
#
# 0 : created from index files - no videos processed yet
# 1 : video processed and active
# 2 : video has been viewed by min_complete_views people (contains this
#     many 'cricket_end's) but the files still exist
# 3 : files have been deleted

video_status_unprocessed = 0
video_status_active = 1
video_status_ready = 2
video_status_finished = 3

#######################################################################
# adding things to the database

def add_cricket(season,cricket_id,tag,sex):
    existing = Cricket.objects.filter(cricket_id=cricket_id)
    if len(existing)!=0:
        #print("not adding, found cricket "+cricket_id)
        return

    print("adding cricket "+cricket_id)
    m = Cricket(cricket_id = cricket_id,
                season = season,
                tag = tag,
                sex = sex)
                
    m.save()

# need to be already split up into chunks
def add_movie(season,camera,index_filename,start_frame,fps,length_frames,start_time,end_time,cricket_id):
    name = start_time.strftime('%Y%m%d')+"-"+str(start_frame);

    existing = Movie.objects.filter(name=name)
    if len(existing)!=0:
        #print("not adding, found movie "+name)
        return


    crickets = Cricket.objects.filter(cricket_id=cricket_id)
    if len(crickets)>0:
        print("adding movie "+name)

        m = Movie(cricket = crickets[0],
                  season = season,
                  name = name,
                  camera = camera,
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

def set_movie_status(moviename,status):
    try:
        existing = Movie.objects.get(name=moviename)
        existing.status = status
        existing.save()
        return True
    except Movie.DoesNotExist:
        return False

def get_movie_status(moviename):
    try:
        existing = Movie.objects.get(name=moviename)
        return existing.status
    except Movie.DoesNotExist:
        return -1

####################################################################
## video processing

# calculate frames and actually do the work, set movie state
def make_video(movie,instance_name):
    print("making "+movie.name)
    frames = robot.exicatcher.read_index(movie.src_index_file)
    frames = frames[movie.start_frame:movie.start_frame+movie.length_frames]
    orig_moviename = os.path.splitext(movie.src_index_file)[0]+".generic.sfs"

    path = str(movie.season)+"/"+movie.camera+"/"
    # check django record exists

    # check subdirectory exists and create it if not
    if not os.path.exists(robot.settings.dest_root+path):
        os.makedirs(robot.settings.dest_root+path)

    # trust the status, so will overwrite existing files
    if movie.status==0:
        robot.exicatcher.extract(orig_moviename, frames, instance_name+"/frame", False)
        robot.process.renamer(movie.start_frame,movie.length_frames,instance_name)
        robot.process.create_thumb(path+movie.name,instance_name)
        robot.process.run_converter(path+movie.name,movie.fps,instance_name)
        robot.process.delete_frames(instance_name)
        movie.status = 1
        movie.save()
    else:
        print(movie.name+": status is 1 - is already done")
        # status is 1 so check files actually exist..
        if not robot.process.check_done(path+movie.name):
            print("status is 1 but no files, setting status to 0, will get next time")
            movie.status = 0
            movie.save()

# new approach to processing, try and keep videos_per_cricket amount of 
# videos always availible - this doesn't delete finished ones though
def process_cricket_video(instance_name):
    cricket = crickets.common.random_one(Cricket)
    #cricket = Cricket.objects.filter(tag="NA")[0]
    # count videos active for this cricket
    videos_ready = Movie.objects.filter(cricket=cricket,status=1).count()
    if videos_ready<robot.settings.videos_per_cricket:
        make_video(Movie.objects.filter(cricket=cricket,status=0).order_by('?')[0],instance_name)
    
def update_video_status():
    for movie in Movie.objects.all():
        path = str(movie.season)+"/"+movie.camera+"/"
        if robot.process.check_done(path+movie.name):
            if movie.status == 0:
                print("found a movie turned off good files, turning on: "+movie.name)
                set_movie_status(movie.name,1)

        if not robot.process.check_done(path+movie.name) and movie.status == 1:
            print("!!! found a movie turned ON without files, turning off: "+movie.name)
            set_movie_status(movie.name,0)

        # is this movie complete?
        if movie.status<2 and movie.views>robot.settings.min_complete_views:
            print(movie.name+" is complete with "+str(movie.views)+" views")
            set_movie_status(movie,2)
            # delete files separately

def update_cricket_status():
    # todo: random selection
    for cricket in Cricket.objects.all():
        videos_ready=0
        # search for active videos
        for movie in Movie.objects.filter(cricket=cricket,
                                          status=video_status_active):
            videos_ready+=1
        cricket.videos_ready=videos_ready
        cricket.save()


def video_clearup():
    for movie in Movie.objects.filter(status=2):
        print(movie.name)
        var = raw_input("Ok to delete "+movie.name+", status:"+str(movie.status)+" with "+str(movie.views)+" views? [y/n] ")
        if var=="y" or var=="Y":
            #print("not deleting "+movie.name)
            robot.process.delete_videos(movie.name)
            set_movie_status(movie,3)

# grab (new) thumbnails from old processed videos
# hopefully only needed temporarily
def update_video_thumbs():
    for movie in Movie.objects.filter(status=1):
        if robot.process.check_done(movie.name):
            robot.process.create_thumb_from_movie(movie.name)

##################################################################
# getting crickets and videos from the source data spreadsheet

# returns the start/end frames for these times
def find_frames_from_index_file(exi_index_file,start_time,end_time):
    if os.path.exists(exi_index_file):
        frames = robot.exicatcher.read_index(exi_index_file)
        state = "searching"
        start = -1
        end = -1
        try:
            for num,f in enumerate(frames):
                t = conv_time(f['time'])            
                if t>start_time and state=="searching":
                    start = num 
                    state = "inside"
                if t>end_time and state=="inside":
                    end = num
                    state = "done"
        except:
            print("error in exi file: "+exi_index_file)

        # over the end of the video
        if end==-1: end=len(frames)-1
        return (start,end)
    else:
        return (-1, -1)

def get_exact_frame_time(exi_frames,frame_num):
    return conv_time(exi_frames[frame_num]['time'])

# chop arbitrary length into videos of the same length
def add_movies(season,camera,start_time,end_time,cricket_id,video_length_secs,fps,tag,sex):
    current_start_time = start_time
    loops = 0
    while current_start_time<end_time:
        exi_index_file = robot.settings.season_to_data_location[season]+"IP"+camera+"/Videos/"+current_start_time.strftime('%Y%m%d')+".index"

        #print("searching for "+exi_index_file)
        frames = find_frames_from_index_file(exi_index_file,current_start_time,end_time)
        start_frame = frames[0]
        end_frame = frames[1]
        total_length_frames = end_frame-start_frame

        # now we need to chop into short videos
        frames_per_video = video_length_secs*fps
        if start_frame!=-1:
            # only bother adding a cricket if there is a video to go with it...
            add_cricket(season,cricket_id,tag,sex)
            
            # reload the frames in so we can find out the precice times
            exi_frames = robot.exicatcher.read_index(exi_index_file)
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

        tomorrow = trunc_time(current_start_time.date()+timedelta(days=1))
        current_start_time=tomorrow
        loops+=1

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
                sex = row[4]
                start = timezone.utc.localize(datetime.strptime(row[5],"%d/%m/%Y %H:%M"))
                end = timezone.utc.localize(datetime.strptime(row[6],"%d/%m/%Y %H:%M"))

                # skip first and last minute
                start += timedelta(minutes=1)
                end -= timedelta(minutes=1)
               
                add_movies(season,camera,start,end,cricket_id,video_length,fps,tag,sex)

def disk_state():
    df = subprocess.Popen(["df", "-h", "/"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    return used+" used, "+available+" available, "+percent+" full"

def generate_report():
    score_text = ""
#    for i,player in enumerate(PlayerBurrowScore.objects.values('player__username').order_by('player').annotate(total=Sum('movies_finished')).order_by('-total')[:10]):
#        score_text += str(i)+" "+player['player__username']+": "+str(player['total'])+"\n"

    crickvid_text = ""
    for cricket in Cricket.objects.all():
        if cricket.videos_ready>0: crickvid_text+=str(cricket.tag)+":"+str(cricket.videos_ready)+" "

    #for m in Movie.objects.filter(cricket__tag="NA",status=1):
    #    crickvid_text+="\n"+m.name+" "+m.camera

    crickvid_text +="\n"

    load = os.getloadavg()

    return "it's yer daily cricket tales 2 robot report\n"+\
    "-------------------------------------------\n"+\
    "\n"+\
    "players: "+str(Player.objects.all().count())+"\n"+\
    "crickets with enough videos ready: "+str(Cricket.objects.exclude(videos_ready__lt=robot.settings.videos_needed_per_cricket).count())+"\n"+\
    "\n"+crickvid_text+"\n"+\
    "movies watched: "+str(Movie.objects.all().aggregate(Sum('views'))['views__sum'])+"\n"+\
    "events recorded: "+str(Event.objects.all().count())+"\n"+\
    "\n"+\
    "movie info\n"+\
    "available: "+str(Movie.objects.filter(status=1).count())+"\n"+\
    "awaiting processing: "+str(Movie.objects.filter(status=0).count())+"\n"+\
    "done but needing deleting: "+str(Movie.objects.filter(status=2).count())+"\n"+\
    "finished: "+str(Movie.objects.filter(status=3).count())+"\n"+\
    "\n"+\
    "top 10 players:\n"+\
    score_text+\
    "\n"+\
    "disk state: "+disk_state()+"\n"+\
    "server load average: "+str(load[0])+" "+str(load[1])+" "+str(load[2])+"\n"+\
    "(eight cpus, so only in trouble with MD if > 8)\n"+\
    """
                     ___ --.   
                   .`   '.  \  
              ,_          | |  
       .''''''|\'.''''''-./-;  
      |__.----| \ '.      |0 \ 
   __/ /  /  /|  \  '.____|__| 
   `''''''''`'|`'''---'|  \    
          .---'        /_  |_  """ 


##############################################################
## event processing

def avg_time(datetimes):
    total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in datetimes)
    return total / len(datetimes)

def plot_activity(event_type):
    arr=[]
    for cricket in Cricket.objects.all():
        times = []
        for event in Event.objects.filter(movie__cricket=cricket,event_type=event_type):
            #print("found "+str(event.estimated_real_time))
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            arr.append(a/(60.0*60.0))
    if len(arr)>1:
        robot.plot.create_plot(np.array(arr),"media/images/autoplots/"+event_type+".png")
    else:
        pass #print("not enough crickets have "+event_type+" to plot")

def plot_moving_activity():
    arr=[]
    for cricket in Cricket.objects.all():
        times = []
        for event in Event.objects.filter(movie__cricket=cricket).filter(Q(event_type="in")|Q(event_type="mid")|Q(event_type="out")):
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            arr.append(a/(60.0*60.0))
    if len(arr)>1:
        robot.plot.create_plot(np.array(arr),"media/images/autoplots/moving.png")
    else:
        pass #print("not enough crickets have moving events to plot")

def test_plot():
    arr=[]
    for i in range(0,1000):
        arr.append(random.uniform(0,4))
    for i in range(0,1000):
        arr.append(random.uniform(18,20))
    robot.plot.create_plot(np.array(arr),"media/images/autoplots/test.png")
    
def calculate_minmax_events(event_type):
    min_events=99999999
    max_events=0
    for cricket in Cricket.objects.all():
        count = len(Event.objects.filter(movie__cricket=cricket,event_type=event_type))
        if count>max_events: max_events=count
        if count<min_events: min_events=count

    existing = Value.objects.filter(name=event_type+"_min")
    if len(existing)!=0:
        existing[0].value = min_events
    else:
        Value.objects.create(name=event_type+"_min",value=min_events)
    existing = Value.objects.filter(name=event_type+"_max")
    if len(existing)!=0:
        existing[0].value = max_events
    else:
        Value.objects.create(name=event_type+"_max",value=max_events)
    
def calculate_minmax_moving():
    min_events=99999999
    max_events=0
    for cricket in Cricket.objects.all():
        count = len(Event.objects.filter(movie__cricket=cricket).filter(Q(event_type="in")|Q(event_type="mid")|Q(event_type="out")))
        if count>max_events: max_events=count
        if count<min_events: min_events=count

    existing = Value.objects.filter(name="moving_min")
    if len(existing)!=0:
        existing[0].value = min_events
        existing[0].save()
    else:
        Value.objects.create(name="moving_min",value=min_events)
    existing = Value.objects.filter(name="moving_max")
    if len(existing)!=0:
        existing[0].value = max_events
        existing[0].save()
    else:
        Value.objects.create(name="moving_max",value=max_events)
    
def calc_daynight_scores():
    for cricket in Cricket.objects.all():
        times = []
        for event in Event.objects.filter(movie__cricket=cricket):
            times.append(event.estimated_real_time)
        if len(times)>0:
            a = avg_time(times)
            cricket.daynight_score=a/(60.0*60.0)
            cricket.save()

###################################################################
## event processing for data reporting

def update_events_actual_real_times():
    for event in Event.objects.filter(actual_real_time__isnull==True):
        frame = event.video_time*robot.settings.video_fps
        frames = robot.exicatcher.read_index(event.movie.src_index_file)
        event.actual_real_time=conv_time(frames[frame]['time'])
        event.save()

def generate_data_report():
    update_events_actual_real_times()
    return ""

# process crickets : videos ready
# (update scores/activity immediately so players see new results)
