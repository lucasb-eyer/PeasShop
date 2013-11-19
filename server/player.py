import json

class Player(object):
    def __init__(self, ws, money_init, game):
        self.ws = ws
        self.money = money_init
        self.game = game
        self.item_dict = {item['id']: item for item in game.item_list}
        self.score = 0.0
        self.bonus = 0.0
    def send(self, msg):
        self.ws.send(json.dumps(msg))

    def can_buy(self, item_id):
        #Get cost
        cost = item_dict[item_id]['price']
        #Get slot
        slot = item_dict[item_id]['type']

        if( self.money >= cost):
            if(slot not in self.slots)
                self.money -= cost
                self.score += self.item_dict[item_id]['rating']
                self.slots[item_dict[item_id]['type']] = item_dict[item_id]

                bon = len(self.slots) > 1
                color = item_dict[item_id]['color']
                for k, v in self.slots :
                    if v['color'] != color :
                        bon = False

                if bon :
                    self.bonus = 3*len(self.slots)
                else :
                    self.bonus = 0
                self.send({'type' : 'you_took', 'item' : item_id, 'money' :
                           self.money, 'score' : self.score},
                          'color_bonus' : self.bonus)
                self.game.opponent(self).send({'type' : 'other_took', 'item' :
                                               item_id, 'other_money' :
                                               self.money, 'other_score' :
                                               self.score,
                                               'other_color_bonus' : self.bonus)
