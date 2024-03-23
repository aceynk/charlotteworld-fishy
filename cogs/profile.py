# main imports
import os
import json
import discord
import operator
import time

import asyncio as asy

from discord.ext import commands, tasks
from functools import reduce

# local imports
import util

def gk(id, key, profile=None):
    if profile is None:
        profile = json.load(open(os.path.join(util.LOC,"profiles.json"),"r"))

    if isinstance(key,list) and not len(key) == 1:
        return reduce(operator.getitem, key, profile[str(id)])
    else:
        if isinstance(key,list): key = key[0]
        return profile[str(id)][key]
    

def sk(id, key, val, profile=None):
    if profile is None:
        profile = json.load(open(os.path.join(util.LOC,"profiles.json"),"r"))

    if isinstance(key,list) and not len(key) == 1:
        gk(id, key[:-1], profile)[key[-1]] = val
    else:
        if isinstance(key,list): key = key[0]
        profile[str(id)][key] = val

    json.dump(profile, open(os.path.join(util.LOC, "profiles.json"),"w"), indent=2)


def ak(id, key, val, profile=None):
    if profile is None:
        profile = json.load(open(os.path.join(util.LOC,"profiles.json"),"r"))

    if isinstance(key,list) and not len(key) == 1:
        cur_val = gk(id, key, profile)
    else:
        if isinstance(key,list): key = key[0]
        cur_val = profile[str(id)][key]

    if isinstance(val, list):
        cur_val.extend(val)
    elif isinstance(val, str):
        cur_val.append(val)
    else:
        cur_val += val

    sk(id, key, round(cur_val,1))


#### cog ####
class profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    def set_id(self, id):
        self.id = str(id)


    @commands.command(
        name="profile", 
        aliases=["p"],
        brief="Allows you to see your profile",
        help="Allows you to see your profile by running !p[rofile].\n Shows stats like your money, fish caught, general items, etc.",
        description="See your profile"
        )
    async def fs_profile(self,ctx):
        util.profile_check(ctx.author)
        util.update_bait(ctx.author)

        acc_id = str(ctx.author.id)
        self.id = acc_id
        fishes = json.load(open(os.path.join(util.LOC,"fishes.json"),"r"))

        output = f"## Fishy Profile for {util.get_nick(ctx.author)}"
        output += f"\nYou have **{round(gk(acc_id, 'money'),1)}** FishCoin(s)"
        output += f"\nYou have **{round(gk(acc_id, 'bait'),1)}** bait."
        output += f"\nYou have **{util.format_time(3600 - (round(time.time()) - gk(acc_id, 'last_bait')))}** until your next bait."
        
        if "optimized_bait" in gk(acc_id, "upgrades") and gk(acc_id, ["upgrades","optimized_bait","amount"]) > 0:
            output += f'\nYou get **{round(1 + 0.2 * gk(acc_id, ["upgrades","optimized_bait","amount"]),1)}** bait per hour'
        
        weights = self.get_base_weights()
        output += f"\n\nYou have a **{weights[0]/10}**% chance to catch a Normal fish."

        if len(set(gk(self.id, "fish").keys()).intersection([x["name"] for x in fishes["difficult"]["catches"]])) > 0:
            output += f"\nYou have a **{round(weights[1]/10,1)}**% chance to catch a *Difficult* fish."
        
        if len(set(gk(self.id, "fish").keys()).intersection([x["name"] for x in fishes["challenging"]["catches"]])) > 0:
            output += f"\nYou have a **{round(weights[2]/10,1)}**% chance to catch a **Challenging** fish."

        if len(set(gk(self.id, "fish").keys()).intersection([x["name"] for x in fishes["legendary"]["catches"]])) > 0:
            output += f"\nYou have a **{round(weights[3]/10,1)}**% chance to catch a *LEGENDARY* fish."

        if gk(self.id, "uniques"):
            output += f"\nYou have a **{round(weights[4]/10,1)}**% chance to catch a **UNIQUE** fish."


        output += "\n"


        for key,val in gk(self.id, ["fish"]).items():
            if val["amount"] > 0:
                output += f"\nYou have **{val['amount']}** {key}(s)! ({emoji.get_emoji(key)})"

        output += "\n"

        for key,val in gk(self.id, ["items"]).items():
            if val["amount"] > 0:
                output += f"\nYou have **{val['amount']}** {key}(s)! ({emoji.get_emoji(key)})"

        if gk(self.id, "uniques"):
            output += "\n\nYou have the following Uniques:\n"

            for i in set(gk(self.id, "uniques")):
                output += f"**{i}**\n"

        for i in util.split_message(output):
            await ctx.send(i)
            await asy.sleep(0.5)


    def add_items(self, items):
        item_set = set(items)

        for item in item_set:
            if item in gk(self.id,"items").keys():
                sk(self.id, ["items",item,"amount"], gk(self.id,["items",item,"amount"]) + items.count(item))
            else:
                sk(self.id, ["items",item], {"amount": items.count(item)})


    def add_fish(self, fish):
        if util.is_unique_fish(fish) or util.is_unique_item(fish):
            ak(self.id, ["uniques"], fish)
        elif fish in gk(self.id,"fish").keys():
            ak(self.id, ["fish",fish,"amount"], 1)
        else:
            sk(self.id, ["fish",fish], {"amount": 1})


    def rm_random(self, items, amount, base_key = []):
        spread_max = []

        items_keys = gk(self.id,base_key).keys()
        for i in items:
            if i in items_keys:
                spread_max.append(gk(self.id, base_key + [i,"amount"]))
            else: spread_max.append(0)

        if amount.lower() == "all":
            amount = sum(spread_max)
        else: amount = int(amount)

        if amount > sum(spread_max):
            return 0

        for i,v in enumerate(util.even_spread(spread_max, amount)):
            if items[i] in items_keys:
                sk(self.id, base_key + [items[i],"amount"], v)
            else:
                sk(self.id, base_key + [items[i]], {"amount": v})

        return amount
    

    def get_base_weights(self):
        if "trash" in gk(self.id,"consumables").keys():
            trash_rec = min(475, gk(self.id,["consumables","trash","amount"]))

            return [950 - 2 * trash_rec, 40 + trash_rec, 6 + trash_rec, 3, 1]
        else:
            return [950, 40, 6, 3, 1]
        

    def clear_weight_bonus(self):
        if "trash" in gk(self.id,"consumables").keys():
            amt = gk(self.id, ["consumables", "trash","amount"])
            if amt > 475:
                ak(self.id, ["consumables","trash","amount"],-475)
            else:
                sk(self.id, ["consumables","trash","amount"],0)


    async def cache_display_names(self):
        profiles = json.load(open(os.path.join(util.LOC,"profiles.json"),"r"))

        guild = await self.bot.fetch_guild(1209999456360202330)
        
        for i in profiles.keys():
            sk(i, "display_name", ((await guild.fetch_member(int(i))).display_name))

    
    @tasks.loop(hours=1.0)
    async def display_loop(self):
        await self.cache_display_names()


#### end cog ####

async def setup(bot):
    # init cog
    cog = profiles(bot)

    global emoji
    emoji = bot.get_cog("emoji")

    await bot.add_cog(cog)