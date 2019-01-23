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

import csv
import datetime

def time_intersection(t1, t2):
    t1start, t1end = t1[0], t1[1]
    t2start, t2end = t2[0], t2[1]
    if t1end < t2start: return False
    if t1end == t2start: return True
    if t1start == t2start: return True
    if t1start < t2start and t2start < t1end: return True
    if t1start > t2start and t1end < t2end: return True
    if t1start < t2start and t1end > t2end: return True
    if t1start < t2end and t1end > t2end: return True
    if t1start > t2start and t1start < t2end: return True
    if t1start == t2end: return True
    if t1end == t2end: return True 
    if t1start > t2end: return False

def import_crickets(filename, make_fn):
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                print row
                name = row[0]
                gender = row[1]
                born = row[2]
                born_at_burrow = row[3]
                mass_at_birth = row[4]
                if born == 'Unknown':
                    born = None
                else:
                    born = datetime.datetime.strptime(born,"%d-%b-%Y")

                make_fn(name,gender,born,born_at_burrow,mass_at_birth)


def import_cameras_to_burrows(filename):
    ret = []
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                ret.append({"camera": row[0],
                            "burrow": row[1],
                            "on": datetime.datetime.strptime(row[2],"%d-%b-%Y  %H:%M"),
                            "off": datetime.datetime.strptime(row[3],"%d-%b-%Y  %H:%M")})
    return ret

# simple linear lookup
def get_burrow(cameras_to_burrows,camera_name,start_time,end_time):
    for c2b in cameras_to_burrows:
        if c2b["camera"] == camera_name and c2b["on"]<start_time and c2b["off"]>end_time:
            return c2b["burrow"]
    return False

def import_cameras_to_traps(filename):
    ret = []
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                ret.append({"year": row[0],
                            "camera": row[1],
                            "start": datetime.datetime.strptime(row[2],"%d/%m/%Y  %H:%M"),
                            "end": datetime.datetime.strptime(row[3],"%d/%m/%Y  %H:%M")})
        return ret

def is_trap_present(cameras_to_traps,camera_name,start_time,end_time):
    for c2t in cameras_to_traps:        
        if c2t["camera"] == camera_name and time_intersection((start_time,end_time), 
                                                              (c2t["start"],c2t["end"])):
            return True
    return False

def connect_cricket_to_movies(filename, connect_fn):
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                id = row[0]
                name = row[1]
                day = row[2]
                burrow = row[3]
                date_in = row[4]
                date_out = row[5]
                date_in = datetime.datetime.strptime(date_in,"%d-%b-%Y  %H:%M")
                date_out = datetime.datetime.strptime(date_out,"%d-%b-%Y  %H:%M")

                connect_fn(name,burrow,date_in,date_out)

