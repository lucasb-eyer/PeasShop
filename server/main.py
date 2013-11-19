from flask import Flask, request, render_template, redirect, url_for
from flask_sockets import Sockets
import random
import string
import json
from game import Game
from player import Player
import requests

app = Flask(__name__)
app.debug = True
app.url_map.strict_slashes = False
sockets = Sockets(app)

#Dictionary of games
game_id_length = 3
game_money_init = 20
game_instances = {}
item_list = None


def render_file(filename, *args, **kwargs):
    return render_template(filename, *args, **kwargs)


@sockets.route('/ws')
def ws(ws):
    # As I can't get query parameters or variable URLs to work,
    # I just let the user send me the gameid.
    gid = ws.receive()
    print("GID: {}".format(gid))

    game = game_instances[gid]
    player = Player(ws, game_money_init, game)

    game.join(player)

    while True:
        message = ws.receive()
        m = json.loads(message)
        if m['type'] == 'wanna':
            player.can_buy(m['id'])


@app.route('/newgame')
def newgame():
    # Create a new game with an id not yet in use
    gid = generate_game_id(game_id_length)
    while gid in game_instances:
        gid = generate_game_id(game_id_length)
    game_instances[gid] = Game(gid, item_list)
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
    return render_file("index.html", new_url=url_for('newgame'))


def generate_game_id(k):
    """ Generates a random alphanumerical id of length k. """
    return "".join(random.sample(string.digits + string.ascii_lowercase, k))


def initialize_item_list():
    """Initializes all the categorie specific item lists."""

    print('Fetching ZALANDO DATA, WITH A D!')
    k_per_category = 20
    item_list = []
    # Here are some constants for the UK shop.
    categories = {'head_category': {'f': ['womens-hats-caps'],
                                    'm': ['mens-hats-caps']},
#                  'body_category': {'m': ['mens-clothing-t-shirts'],
#                                    'f': ['womens-clothing-tops']},
#                  'trouser_category': {'f': ['womens-clothing-mini-skirts'],
#                                       'm': ['mens-clothing-trousers']},
#                  'shoes_category': {'m': ['mens-shoes'],
#                                     'f': ['womens-shoes']},
#                  'accesories_category': {'n': ['accessories',
#                                                'bags-accessories-womens' ]},
                  'special_category': {'n': ['strings-thongs']}}

    for c, d in categories.items():
        for g, cat_list in d.items():
            for cat in cat_list:
                item_list_temp =   get_k_items_from_category(
                     k_per_category, cat,
                     c, g)
                item_list += item_list_temp

    print('Done, WITH A D!')
    random.shuffle(item_list)
    return item_list


def get_k_items_from_category(
    k, category, type, gender, domain_url='www.zalando.co.uk',
        api='https://shop-catalog-api.zalando.net'):
    """Gets k items from a category
    1. Take a category
    2. Load 100 items
    3. Sample k/10+1 of the 100
    4. goto 1. until done
    """

    res = []
    page = 1
    while len(res) < k:
        query = '{}/search/{}/{}/?page={}&?sort=rating'.format(
            api, domain_url, category, page)
        search = requests.get(query, headers={'Accept': 'application/json'})
        items = search.json()
        for i in range(k):
            #     for i in range(k/3 + 1):
            rand_index = random.randint(0, 99)
            sku = items[u'searchResults'][u'data'][rand_index][u'sku']
            article_query = '{}/article/{}/{}'.format(api, domain_url, sku)
            article = requests.get(article_query, headers={
                                   'Accept': 'application/json'})
            # if(article.json()[u'averageRating'] > 0.0):
            article_dict = {'type': type}
            article_dict['name'] = article.json()[u'name']
            article_dict['img_url'] = article.json()[u'images'][u'detailUrl']
            price = article.json()[u'price']
            if( price < 20):
                article_dict['price'] = 1
            elif( price < 45 ):
                article_dict['price'] = 2
            elif( price < 80 ):
                article_dict['price'] = 3
            elif( price < 150 ):
                article_dict['price'] = 4
            else:
                article_dict['price'] = 5

            if( random.uniform(0.0, 1.0) > 0.8):
                article_dict['price'] = random.randint(1,5)
            article_dict['rating'] = random.uniform(0.0, 5.0)
            article_dict['color'] = article.json()[u'color']
            article_dict['gender'] = gender
            article_dict['speed'] = random.uniform(0.1, 1.0) * 0.5 +  0.1 * article_dict['rating']
            article_dict['id'] = sku
            res.append(article_dict)

        page += 1

    return  res


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    item_list = initialize_item_list()

    port = 9000
    print("Gonna listen on port {}".format(port))

    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()


