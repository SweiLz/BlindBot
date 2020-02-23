from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('json')
def handle_json(json):
    print('received json {}'.format(json))


if __name__ == "__main__":
    socketio.run(app)
    # app.run(host='localhost', port=23423)
