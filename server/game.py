import requests
import random


class Game(object):

    def __init__(self, game_id):
        self.game_id = game_id
        self.item_list = []

    def initialize_item_lists(self, n):
        """Initializes all the categorie specific item lists.

        Each lists will contain 2n items from a specific category after this
        finished. n items for men and n items for women, or 2n if no gender
        specific categories are specified.

        """

        k_per_category = 20

        # Here are some constants for the UK shop.
        categories = {'head_category': {'f': ['womens-hats-caps'],
                                        'm': ['mens-hats-caps']},
                      'body_category': {'m': ['mens-clothing-t-shirts'],
                                        'f': ['womens-clothing-tops']},
                      'trouser_category': {'f': ['womens-clothing-mini-skirts'],
                                           'm': ['mens-clothing-trousers']},
                      'shoes_category': {'m': ['mens-shoes'],
                                         'f': ['womens-shoes']},
                      'accesories_category': {'n': ['accessories',
                                                    'bags-accessories-womens' ]},
                      'special_category': {'n': ['strings-thongs']}}

        for c, d in categories.items():
            for g, cat_list in d.items():
                for cat in cat_list:
                    self.item_list += get_k_items_from_category(
                        k_per_category, cat,
                        c, g)


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
        print(len(res))
        query = '{}/search/{}/{}/?page={}&?sort=rating'.format(
            api, domain_url, category, page)
        print(query)
        search = requests.get(query, headers={'Accept': 'application/json'})
        items = search.json()
        for i in range(k/3 + 1):
            rand_index = random.randint(0, 99)
            sku = items[u'searchResults'][u'data'][rand_index][u'sku']
            article_query = '{}/article/{}/{}'.format(api, domain_url, sku)
            article = requests.get(article_query, headers={
                                   'Accept': 'application/json'})
            # if(article.json()[u'averageRating'] > 0.0):
            article_dict = {'type': type}
            article_dict['name'] = article.json()[u'name']
            article_dict['img_url'] = article.json()[u'images'][u'detailUrl']
            article_dict['price'] = article.json()[u'price']
            article_dict['rating'] = random.uniform(0.0, 5.0)
            article_dict['color'] = article.json()[u'color']
            article_dict['gender'] = gender
            # print(article_dict)
            res.append(article_dict)
        page += 1

    return  res
