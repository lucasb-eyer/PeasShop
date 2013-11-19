class Game(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = []

    def join(self, player):
        self.players.append(player)
        self.broadcast({"type": "join", "name": "Anon"})

        if len(self.players) == 2:
            FAKE_ITEMS = [
                {"type": "shoe", "color": "red"},
                {"type": "shoe", "color": "blue"},
                {"type": "shoe", "color": "black"},
                {"type": "shoe", "color": "yellow"},
            ]
            self.broadcast({
                "type": "start",
                "items": FAKE_ITEMS,
            })

    def broadcast(self, msg):
        for player in self.players:
            player.send(msg)
