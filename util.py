# main imports
import os
import random
import math
import json
import time

# local imports
import botstate
from cogs.profile import sk,ak

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
    out_l = []
    while string != "":
        test_split = string[:2000]
        first_nl = test_split[::-1].index("\n")
        out_l.append(string[:2000-first_nl])
        string = string[2000-first_nl:]

    return out_l

def profile_check(user):
    profile = json.load(open(os.path.join(LOC, "profiles.json"),"r"))
    base_profile = json.load(open(os.path.join(LOC, "base_profile.json"),"r"))

    if not str(user.id) in profile.keys():
        profile[str(user.id)] = base_profile

    json.dump(profile, open(os.path.join(LOC, "profiles.json"),"w"), indent=2)

def update_bait(user):
    profile = json.load(open(os.path.join(LOC, "profiles.json"),"r"))

    user_profile = profile[str(user.id)]
    if user_profile["last_bait"] == -1:
        sk(user.id, "bait", 1)
        sk(user.id, "last_bait", round(time.time()))
    else:
        hours_since = (round(time.time()) - user_profile["last_bait"]) // 3600
        seconds_since_update = (round(time.time()) - user_profile["last_bait"]) - 3600 * hours_since

        ak(user.id, "bait", min(48,hours_since))
        sk(user.id, "last_bait", round(time.time()) - seconds_since_update)

def format_time(s):
    output = []
    if s >= 3600:
        output.append(f"{s // 3600} hour(s)")
        s %= 3600
    
    if s >= 60:
        output.append(f"{s // 60} minute(s)")
        s %= 60

    if s:
        output.append(f"{s} second(s)")

    return ", ".join(output)