# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import config
import jaurim
from youtube_api import YoutubeAPI

app = Flask(__name__)
app.secret_key = "secret"
app.debug = True
socketio = SocketIO(app)
youtube = YoutubeAPI({'key': config.YOUTUBE_API})

album_list_index = 0

@app.route('/')
def index():
    return render_template('index.html', music_list=jaurim.music_list)


@app.route('/play/<song>')
def play(song):
    global album_list_index
    song_list_index = int(song)
    target = "자우림 " + str(album_list_index) + "집 " +\
        str(jaurim.music_list[album_list_index-1][song_list_index-1])
    video_list = youtube.search_videos(target)
    video_id = video_list[0]['id']['videoId']
    socketio.emit("response", {
        'type': 'Play',
        'data': video_id,
        'index': song_list_index,
        },
        namespace='/mynamespace',
        broadcast=True)
    return 'Get Song'


@app.route('/select/<album>')
def select(album):
    global album_list_index
    album_list_index = int(album)
    socketio.emit("response", {
        'type': 'Select',
        'data': album,
        'index': album_list_index,
        },
        namespace='/mynamespace',
        broadcast=True)
    return 'Get Song'


@socketio.on('connect', namespace='/mynamespace')
def connect():
    print "Connect"
    emit("response", {
        'type': 'System',
        'data': 'Connected'
    })


@socketio.on('disconnect', namespace='/mynamespace')
def disconnect():
    print "Disconnect"

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=8080
    )
