dest_root = "media/movies/"
outputcsv = "media/data/events.csv"
video_length = 30
video_fps = 10
videos_per_cricket = 10 # less than this kicks off a generate
videos_needed_per_cricket = 2 # minumum for registering as ready
srccsv = "data/VideosSingleCricketsKnownID.csv"
# controls the video file recycling
min_complete_views = 3
season_to_data_location = {"2012": "",
                           "2013": "/synology/nas3.v1/Storage/2013 video/",
                           "2014": "",
                           "2015": "",
                           "2016": "",
                           "2017": ""}
