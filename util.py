# main imports
import os
import random
import discord

# local imports
import botstate

LOC = os.path.split(os.path.realpath(__file__))[0]


def is_mod(ctx) -> bool:
    if ctx.author.id in botstate.get_key("trusted"):
        return True
    return False

adj_fish = ["Shining","Sparkly","Dull","Dark","Scaley","Squishy","Cranky","Froglike","Silly","Beautiful","Stunning"]
noun_fish = ["Trout","Cod","Slug","Urchin","Jellyfish","Ray","Shell"]
adj_item = ["Sparkly","Shining","Golden","Gleaming","Old","Rusted","Dark","Shadowed","Ancient","Forgotten"]
noun_item = ["Shield","Debris","Sword","Clock","Knife","Key"]


def get_unique_fish():
    return random.choice(adj_fish) + " " + random.choice(noun_fish)


def get_unique_item():
    return random.choice(adj_item) + " " + random.choice(noun_item)


def is_unique_fish(item):
    item_spl = item.split()

    if item_spl[0] in adj_fish and item_spl[1] in noun_fish:
        return True
    return False


def is_unique_item(item):
    item_spl = item.split()

    if item_spl[0] in adj_item and item_spl[1] in noun_item:
        return True
    return False


def sanitize(string:str):
    string = string.replace("@","\@")
    string = string.replace("#","\#")
    string = string.replace("@everyone","@\everyone")

    return string


def get_nick(user):
    return sanitize(user.display_name)


def even_spread(l_max, amount):
    d_am = min(min(l_max),amount // len(l_max))
    l_max = [x - d_am for x in l_max]
    amount -= d_am * len(l_max)

    pos = 0
    while amount != 0:
        if l_max[pos] == 0:
            pos += 1
            pos %= len(l_max)
            continue

        l_max[pos] -= 1
        amount -= 1
        pos += 1
        pos %= len(l_max)
    
    return l_max

def split_message(string):
    return [string[i:i+min(len(string) - 2000*i, 2000)] for i in range(0, len(string), 2000)]