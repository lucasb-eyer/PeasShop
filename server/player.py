import json

class Player(object):
    def __init__(self, ws):
        self.ws = ws

    def send(self, msg):
        self.ws.send(json.dumps(msg))
