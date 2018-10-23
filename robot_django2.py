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
import time
import robot.exicatcher
import robot.process
import robot.settings
import crickets.common

django.setup()

# convert time from exicatcher to datetime format
def conv_time(t):
    return timezone.utc.localize(datetime(t[0],t[1],t[3],t[4],t[5],t[6],t[7]/1000))

#######################################################################
# a note on movie status flag:
#
# 0 : created from index files - no videos processed yet
# 1 : video processed and active
# 2 : video has been viewed by min_complete_views people (contains this
#     many 'cricket_end's) but the files still exist
# 3 : files have been deleted
#
#######################################################################


##################################################################
# adding things to the database

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
    name = start_time.strftime('%Y%m%d')+"-"+str(start_frame);

    existing = Movie.objects.filter(name=name)
    if len(existing)!=0:
        print("not adding, found movie "+name)
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
        if not robot.process.check_done(movie.name):
            print("status is 1 but no files, setting status to 0, will get next time")
            movie.status = 0
            movie.save()

def process_random_video(instance_name):
    # pick a random one, also checks already processed ones
    make_video(crickets.common.random_one(Movie),instance_name)

def process_loop(instance_name):
    while True:
        process_random_video(instance_name)
        time.sleep(20)

def update_video_status():
    for movie in Movie.objects.all():
        if robot.process.check_done(movie.name):
            #if not robot.process.check_video_lengths(movie.name):
            #    print("movies too short: "+movie.name)#
            #    print(robot.process.get_video_length(robot.settings.dest_root+movie.name+".mp4"))
            #    print(robot.process.get_video_length(robot.settings.dest_root+movie.name+".ogg"))
            #    print(robot.process.get_video_length(robot.settings.dest_root+movie.name+".webm"))
            #    force redo
            #    set_movie_status(movie.name,0)

            if movie.status == 0:
                print("found a movie turned off good files, turning on: "+movie.name)
                set_movie_status(movie.name,1)

        if not robot.process.check_done(movie.name) and movie.status == 1:
            print("!!! found a movie turned ON without files, turning off: "+movie.name)
            set_movie_status(movie.name,0)

        # is this movie complete?
        if movie.status<2 and movie.views>robot.settings.min_complete_views:
            print(movie.name+" is complete with "+str(movie.views)+" views")
            set_movie_status(movie,2)
            # spawn a video process
            #Thread(target = process_loop, args = ("thread-0", )).start()
            # delete files separately

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
        for num,f in enumerate(frames):
            t = conv_time(f['time'])            
            if t>start_time and state=="searching":
                start = num 
                state = "inside"
            if t>end_time and state=="inside":
                end = num
                state = "done"
        # over the end of the video
        if end==-1: end=len(frames)-1
        return (start,end)
    else:
        return (-1, -1)

def get_exact_frame_time(exi_frames,frame_num):
    return conv_time(exi_frames[frame_num]['time'])

# chop arbitrary length into videos of the same length
def add_movies(season,camera,start_time,end_time,cricket_id,video_length_secs,fps,tag,gender):
    exi_index_file = robot.settings.season_to_data_location[season]+"IP"+camera+"/Videos/"+start_time.strftime('%Y%m%d')+".index"

    frames = find_frames_from_index_file(exi_index_file,start_time,end_time)
    start_frame = frames[0]
    end_frame = frames[1]
    total_length_frames = end_frame-start_frame

    # now we need to chop into short videos
    frames_per_video = video_length_secs*fps
    if start_frame!=-1:
        # only bother adding a cricket if there is a video to go with it...
        add_cricket(season,cricket_id,tag,gender)

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

                add_movies(season,camera,start,end,cricket_id,video_length,fps,tag,gender)

def disk_state():
    df = subprocess.Popen(["df", "-h", "/"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    return used+" used, "+available+" available, "+percent+" full"

def generate_report():
    cricket_end = EventType.objects.filter(name="Cricket End").first()

    score_text = ""
#    for i,player in enumerate(PlayerBurrowScore.objects.values('player__username').order_by('player').annotate(total=Sum('movies_finished')).order_by('-total')[:10]):
#        score_text += str(i)+" "+player['player__username']+": "+str(player['total'])+"\n"

    load = os.getloadavg()

    return "it's yer daily cricket tales 2 robot report\n"+\
    "-------------------------------------------\n"+\
    "\n"+\
    "players: "+str(Player.objects.all().count())+"\n"+\
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
       .""""""|\'.""""""-./-;
      |__.----| \ '.      |0 \
   __/ /  /  /|  \  '.____|__|
   `""""""""`"|`""'---'|  \
          .---'        /_  |_"""


# process crickets : videos ready
# (update scores/activity immediately so players see new results)
