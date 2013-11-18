from flask import Flask, request, render_template
from flask_sockets import Sockets

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)


def render_file(filename, *args, **kwargs):
    return render_template(filename, *args, **kwargs)


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/game/<gameid>')
def game(gameid):
    return render_file("game.html", url=request.url)


@app.route('/')
def hello():
    return render_file("index.html")


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    port = 8000
    print("Gonna listen on port {}".format(port))

    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
