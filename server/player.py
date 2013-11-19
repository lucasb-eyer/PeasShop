import json

class Player(object):
    def __init__(self, ws, money_init, game):
        self.ws = ws
        self.money = money_init
        self.game = game
        self.item_dict = {item['id']: item for item in game.item_list}

    def send(self, msg):
        self.ws.send(json.dumps(msg))

    def can_buy(self, item_id):
        #Get cost
        cost = item_dict[item_id]['price']
        #Get slot
        coste = item_dict[item_id]['item']

        if( self.money >= cost):
            self.money -= cost
            self.slots[item_dict[item_id]['type']] = item_dict[item_id]
            self.send({'type' : 'you_took', 'item' : item_id})
            self.game.opponent(self).send({'type' : 'other_took', 'item' : item_id})
