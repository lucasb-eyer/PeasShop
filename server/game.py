import requests
import random


class Game(object):

    def __init__(self, game_id, item_list):
        self.game_id = game_id
        self.item_list = item_list
        self.players = []

    def join(self, player):
        self.players.append(player)
        self.broadcast({"type": "join", "name": "Anon"})

        if len(self.players) == 2:
            self.broadcast({
                "type": "start",
                "items": self.item_list,
            })

    def broadcast(self, msg):
        for player in self.players:
            player.send(msg)

    def opponent(self, me):
        if self.players[0] == me:
            return self.players[1]
        else:
            return self.players[0]

    def checkwin(self):
        if self.players[0].finished() and self.players[1].finished():
            if self.players[0].score + self.players[0].bonus > self.players[1].score + self.players[1].bonus:
                self.players[0].send({'type': 'win'})
                self.players[1].send({'type': 'lose'})
            else:
                self.players[0].send({'type': 'lose'})
                self.players[1].send({'type': 'win'})
