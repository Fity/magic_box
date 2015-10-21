# -*- coding:utf-8 -*-
import codecs
from collections import defaultdict
from decimal import Decimal
import random


meat_set = set()
vegetable_set = set()
hot_set = set()
cold_set = set()
drinks_set = set()


class Dish(object):

    def __init__(self):
        self.name = None
        self.is_drinks = False
        self.is_meat = None
        self.is_hot = None
        self.score = -1
        self.price = -1

    def __hash__(self):
        return hash(self._get_hash_key())

    def __eq__(self, other):
        return self._get_hash_key() == other._get_hash_key()

    def _get_hash_key(self):
        u'{}-{}-{}-{}'.format(self.name, self.is_meat, self.is_hot,
                              self.is_drinks)

    @classmethod
    def create_from_line(cls, line):
        line = line.strip()
        if not line:
            return None
        dish = cls()
        line = line.split(',')
        dish.name = line[0].strip()
        if line[1] == u'热':
            dish.is_hot = True
        elif line[1] == u'凉':
            dish.is_hot = False
        else:
            dish.is_drinks = True
        if line[2] == u'荤':
            dish.is_meat = True
        elif line[2] == u'素':
            dish.is_meat = False
        dish.score = int(line[3])
        dish.price = Decimal(line[4])
        return dish

    def __str__(self):
        return self.name.encode('utf-8')

    def __repr__(self):
        return u'{}-{}-{}-{}'.format(self.name, self.is_drinks, self.is_meat,
                                     self.is_hot).encode('utf-8')


class Menu(object):

    def __init__(self, people_count):
        self.dish_dict = defaultdict(int)
        self.people_count = people_count

    def __str__(self):
        return u'\n'.join(u'{}-{}份'.format(str(dish), self.dish_dict[dish])
                          for dish in self.dish_dict)

    def add(self, dish):
        if len(self.dish_dict) > self.people_count:
            raise Exception(u'菜点太多吃不完啦')
        if self.validate(dish):
            self.dish_dict[dish] += 1

    def clear(self):
        self.dish_dict.clear()

    def validate(self, dish):
        return True

    def generate(self):
        # drinks
        for _ in xrange(self.get_drink_count()):
            drinks = self.filter_drinks()
            dish = random.choice(drinks)
            self.add(dish)
        print 'drinks'

        # cold foods
        for _ in xrange(self.get_cold_food_count()):
            cold_foods = self.filter_cold_foods()
            dish = random.choice(cold_foods)
            self.add(dish)

        meat_foods = set()
        vegetable_foods = set()
        food_count = 0
        while food_count < self.get_hot_food_count():
            hot_foods = self.filter_hot_foods()
            if dish in meat_foods or dish in vegetable_foods:
                continue
            dish = random.choice(hot_foods)
            try:
                self.add(dish)
                print 'hhh'
            except Exception:
                return
            if dish.is_meat:
                meat_foods.add(dish)
            else:
                vegetable_foods.add(dish)

    def get_hot_food_count(self):
        return self.people_count + 1 - self.get_cold_food_count()

    def get_drink_count(self):
        return max(1, int(self.people_count / 4))

    def get_cold_food_count(self):
        return max(1, int(self.people_count / 4))

    def filter_foods(self, food_set, min_score):
        return list({food for food in food_set
                     if food.score >= min_score})

    def filter_drinks(self):
        global drinks_set
        min_score = 6
        return self.filter_foods(drinks_set, min_score)

    def filter_cold_foods(self):
        global cold_set
        min_score = 6
        return self.filter_foods(cold_set, min_score)

    def filter_hot_foods(self):
        global hot_set
        min_score = 6
        return self.filter_foods(hot_set, min_score)


def load_data():
    with codecs.open('dishes', 'r', 'utf-8') as f:
        for line in f:
            dish = Dish.create_from_line(line.strip())
            if not dish:
                continue
            if dish.is_drinks:
                drinks_set.add(dish)
                continue
            if dish.is_meat:
                meat_set.add(dish)
            else:
                vegetable_set.add(dish)
            if dish.is_hot:
                hot_set.add(dish)
            else:
                cold_set.add(dish)


def generate_menu(people_count):
    menu = Menu(people_count)
    menu.generate()
    return menu


def main():
    load_data()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--count',
        dest='people_count', default=5)
    args = parser.parse_args()
    print generate_menu(args.people_count)


if __name__ == '__main__':
    main()
