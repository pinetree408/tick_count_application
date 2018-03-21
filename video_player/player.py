from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "secret"
app.debug = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/seek/<seconds>')
def seek(seconds):
    socketio.emit("response", {
        'type': 'Seek',
        'data': seconds,
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
    socketio.run(app)
