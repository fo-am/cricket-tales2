#!/usr/bin/env python
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
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

import robot_django2
import robot.process
import robot.movie
import robot.settings
import robot.import_data
import time
from threading import Thread

report_recipients = ["dave@fo.am",
#                     "amber@fo.am",
#                     "T.Tregenza@exeter.ac.uk"
]

def send_email(f,to,subject,text):
    for recipient in to:
        msg = MIMEText(text)
        msg["From"] = f
        msg["To"] = recipient
        msg["Subject"] = subject
        p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        p.communicate(msg.as_string())


if len(sys.argv)<2 or sys.argv[1]=="-?" or sys.argv[1]=="--help":
    print "Welcome to the cricket tales processing robot v0.0.1"
else:
    if sys.argv[1]=="import-crickets":
        robot_django2.import_crickets(robot.settings.srccsv,
                                      robot.settings.video_length,
                                      robot.settings.video_fps)
    if sys.argv[1]=="process-one-video":
        robot_django2.process_random_video("thread-0")
    if sys.argv[1]=="video-process":
        Thread(target = robot_django2.process_loop, args = ("thread-0", )).start()
        Thread(target = robot_django2.process_loop, args = ("thread-1", )).start()
        Thread(target = robot_django2.process_loop, args = ("thread-2", )).start()
        Thread(target = robot_django2.process_loop, args = ("thread-3", )).start()
        Thread(target = robot_django2.process_loop, args = ("thread-4", )).start()
        Thread(target = robot_django2.process_loop, args = ("thread-5", )).start()
    if sys.argv[1]=="update":
        robot_django2.update_cricket_status()
        robot_django2.update_video_status()
        robot_django2.test_plot()
        robot_django2.plot_activity("singing")
        robot_django2.plot_activity("eating")
        robot_django2.plot_moving_activity()
        robot_django2.calc_daynight_scores()
        
    if sys.argv[1]=="video-clearup":
        robot_django.video_clearup()

    # if sys.argv[1]=="activity-update":
    #     robot_django.update_all_activity()
    # if sys.argv[1]=="movie-update":
    #     robot_django.update_movies()
    if sys.argv[1]=="print-report":
         print(robot_django2.generate_report())
    if sys.argv[1]=="report":
        report = robot_django2.generate_report()
        send_email("robot@cricket-tales.ex.ac.uk",
                   report_recipients,"cricket tales report",
                   report)
    if sys.argv[1]=="overwrite-thumbnails":
        robot_django.update_video_thumbs()
    if sys.argv[1]=="test":
        robot_django2.calculate_minmax_events("singing")
        robot_django2.calculate_minmax_events("eating")
        robot_django2.calculate_minmax_moving()
