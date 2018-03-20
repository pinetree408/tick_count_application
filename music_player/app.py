# -*- coding: utf-8 -*-
import serial
import requests
import config
import jaurim
from youtube_api import YoutubeAPI

cur_degree = 10
cur_dir = 1

boundary = 10
baseline = 11
twomode = 12
chunk = 13

song_list_index = 0
album_list_index = 0

youtube = YoutubeAPI({'key': config.YOUTUBE_API})

with serial.Serial('/dev/tty.usbmodem1411', 115200) as ser:
    ser.write(bytes(str(cur_degree) + ' ' + str(twomode)  + ' ' + str(cur_dir) + '\n'))
    while (True):
        first = ser.read()
        if (first == 'x'):
            if (ser.read() == 'x'):
                if (ser.read() == 'x'):
                    s = ser.readline()
                    data_list = s.split(' ')
                    index_finger = int(data_list[1])
                    middle_finger = int(data_list[2])
                    tick_count = int(data_list[3])
                    tick_count_middle = int(data_list[4])
                    is_tap = int(data_list[5])

                    if index_finger == 1:
                        song_list_index = tick_count
                    elif middle_finger == 1:
                        album_list_index =  tick_count_middle

                    if is_tap == 1:
                        if album_list_index > 0 and song_list_index > 0:
                            target = "자우림 " + str(album_list_index) + "집 " + str(jaurim.music_list[album_list_index-1][song_list_index-1])
                            album_list_index = -1
                            song_list_index = -1
                            video_list = youtube.search_videos(target)
                            video_id = video_list[0]['id']['videoId']
                            print target
                            requests.get('http://localhost:5000/play/' + video_id)
                            album_list_index = 0
                            song_list_index = 0
                        elif album_list_index > 0 and song_list_index == 0:
                            requests.get('http://localhost:5000/select/' + str(album_list_index))
