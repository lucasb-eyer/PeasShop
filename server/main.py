from flask import Flask, request, render_template, redirect, url_for
from flask_sockets import Sockets
import random
import string
import json
from game import Game
from player import Player

app = Flask(__name__)
app.debug = True
app.url_map.strict_slashes = False
sockets = Sockets(app)

#Dictionary of games
game_id_length = 3
game_instances = {}


def render_file(filename, *args, **kwargs):
    return render_template(filename, *args, **kwargs)


@sockets.route('/ws')
def ws(ws):
    # As I can't get query parameters or variable URLs to work,
    # I just let the user send me the gameid.
    gid = ws.receive()
    print("GID: {}".format(gid))

    game = game_instances[gid]
    player = Player(ws)

    game.join(player)

    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/newgame')
def newgame():
    # Create a new game with an id not yet in use
    gid = generate_game_id(game_id_length)
    while gid in game_instances:
        gid = generate_game_id(game_id_length)
    game_instances[gid] = Game(gid)
    return redirect(url_for('game', gameid=gid))


@app.route('/game/<gameid>')
def game(gameid):
    if gameid in game_instances:
        #This game exist.
        return render_file("game.html", url=request.url)
    else:
        #This game doesn't exist yet, just redirect to the main page.
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_file("index.html", new_url=url_for('new_game'))


def generate_game_id(k):
    """ Generates a random alphanumerical id of length k. """
    return "".join(random.sample(string.digits + string.ascii_lowercase, k))

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    port = 9000
    print("Gonna listen on port {}".format(port))

    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
