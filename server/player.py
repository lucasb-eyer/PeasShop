import json

class Player(object):
    def __init__(self, ws, money_init, game):
        self.ws = ws
        self.money = money_init
        self.game = game
        self.item_dict = {item['id']: item for item in game.item_list}
        self.slots = {}

    def send(self, msg):
        self.ws.send(json.dumps(msg))

    def can_buy(self, item_id):
        #Get cost
        cost = self.item_dict[item_id]['price']
        slot = self.item_dict[item_id]['type']

        if self.money >= cost:
            if slot not in self.slots:
                self.money -= cost
                self.slots[slot] = self.item_dict[item_id]
                self.send({'type' : 'you_took', 'item' : item_id, 'money' :
                           self.money})
                self.game.opponent(self).send({'type' : 'other_took', 'item' :
                                               item_id, 'other_money' :
                                               self.money})
