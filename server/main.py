from flask import Flask, request, render_template, redirect
from flask_sockets import Sockets
import random
import string
from game import Game

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)

#Dictionary of games
game_id_length = 3
game_instances = {}


def render_file(filename, *args, **kwargs):
    return render_template(filename, *args, **kwargs)


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/game')
def new_game():
    # Create a new game with an id not yet in use
    new_game_id = generate_game_id(game_id_length)
    while new_game_id in game_instances:
        new_game_id = generate_game_id(game_id_length)
    game_instances[new_game_id] = Game(new_game_id)
    return redirect('/game/{}'.format(new_game_id))


@app.route('/game/<gameid>')
def game(gameid):
    return render_file("game.html", url=request.url)


@app.route('/')
def hello():
    return render_file("index.html")


def generate_game_id(k):
    """ Generates a random alphanumerical id of length k. """
    return "".join(random.sample(string.digits + string.ascii_lowercase, k))

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    port = 8000
    print("Gonna listen on port {}".format(port))

    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
