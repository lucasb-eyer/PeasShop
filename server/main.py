from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)


def render_file(filename, *args, **kwargs):
    s = open(filename).read()
    # TODO: string/replace in s, cheap .50$ templates.
    return s


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def hello():
    return render_file("template/index.html")
