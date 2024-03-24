# main imports
import os
import json
import discord
import operator
import time
import random

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
    async def fs_profile(self,ctx,user: discord.Member = None):
        if not (user is None):
            acc_id = str(user.id)
            self.id = acc_id

            try: 
                # works like an assert statement
                # smth like:
                # assert "pronouns" in user profile
                # also assigns to a variable :D
                pronouns = gk(acc_id,"pronouns")

                index = random.randrange(len(pronouns["subject"]))

                reference = [
                    pronouns["subject"][index],
                    pronouns["possessive"][index],
                    pronouns["have"][index]
                ]
            except Exception as e:
                print(e)
                reference = ["They","Their","have"]

        else:
            util.profile_check(ctx.author)
            util.update_bait(ctx.author)

            acc_id = str(ctx.author.id)
            self.id = acc_id

            user = ctx.author

            reference = ["You","Your","have"]

        fishes = json.load(open(os.path.join(util.LOC,"fishes.json"),"r"))

        output = f"## Fishy Profile for {util.get_nick(user)}"
        output += f"\n{reference[0].title()} {reference[2].lower()} **{round(gk(acc_id, 'money'),1)}** FishCoin(s)"
        output += f"\n{reference[0].title()} {reference[2].lower()} **{round(gk(acc_id, 'bait'),1)}** bait."
        if round(time.time()) - gk(acc_id, 'last_bait') <= 3600:
            output += f"\n{reference[0].title()} {reference[2].lower()} **{util.format_time(3600 - (round(time.time()) - gk(acc_id, 'last_bait')))}** until your next bait."
        else: 
            output += f"\n{reference[0].title()} {reference[2].lower()} **{util.format_time(3600 - (round(time.time()) - gk(acc_id, 'last_bait')) % 3600)}** until {reference[1].lower()} next bait."

        if "optimized_bait" in gk(acc_id, "upgrades") and gk(acc_id, ["upgrades","optimized_bait","amount"]) > 0:
            output += f'\n{reference[0].title()} {"gets" if reference[2].endswith("s") else "get"} **{round(1 + 0.2 * gk(acc_id, ["upgrades","optimized_bait","amount"]),1)}** bait per hour.'

        if "estrogen" in gk(acc_id, "upgrades") and gk(acc_id, ["upgrades","estrogen","amount"]) > 0:
            output += f'\n{reference[0].title()} {reference[2].lower()} **{gk(acc_id, ["upgrades","estrogen","amount"])}** estrogen!'
        
        weights = self.get_base_weights()
        output += f"\n\n{reference[0].title()} {reference[2].lower()} a **{weights[0]/10}**% chance to catch a Normal fish."

        if len(set(gk(self.id, "fish").keys()).intersection([x["name"] for x in fishes["difficult"]["catches"]])) > 0:
            output += f"\n{reference[0].title()} {reference[2].lower()} a **{round(weights[1]/10,1)}**% chance to catch a *Difficult* fish."
        
        if len(set(gk(self.id, "fish").keys()).intersection([x["name"] for x in fishes["challenging"]["catches"]])) > 0:
            output += f"\n{reference[0].title()} {reference[2].lower()} a **{round(weights[2]/10,1)}**% chance to catch a **Challenging** fish."

        if len(set(gk(self.id, "fish").keys()).intersection([x["name"] for x in fishes["legendary"]["catches"]])) > 0:
            output += f"\n{reference[0].title()} {reference[2].lower()} a **{round(weights[3]/10,1)}**% chance to catch a *LEGENDARY* fish."

        if gk(self.id, "uniques"):
            output += f"\n{reference[0].title()} {reference[2].lower()} a **{round(weights[4]/10,1)}**% chance to catch a **UNIQUE** fish."


        output += "\n"


        for key,val in gk(self.id, ["fish"]).items():
            if val["amount"] > 0:
                output += f"\n{reference[0].title()} {reference[2].lower()} **{val['amount']}** {key}(s)! ({emoji.get_emoji(key)})"

        output += "\n"

        for key,val in gk(self.id, ["items"]).items():
            if val["amount"] > 0:
                output += f"\n{reference[0].title()} {reference[2].lower()} **{val['amount']}** {key}(s)! ({emoji.get_emoji(key)})"

        if gk(self.id, "uniques"):
            output += f"\n\n{reference[0].title()} {reference[2].lower()} the following Uniques:\n"

            for i in set(gk(self.id, "uniques")):
                output += f"**{i}**\n"

        for i in util.split_message(output):
            await ctx.send(i)
            await asy.sleep(0.5)


    @commands.command(
        name="trade",
        aliases=["gift"],
        brief="Trade items",
        help="Trade items with another player! Use ![trade|gift] <amount> <item> <user>\nThe user parameter works with many inputs, including ids and pings!",
        description="The trade command"
    )
    async def fs_trading(self,ctx,amt,item,user:discord.Member):
        key_locs = json.load(open(os.path.join(util.LOC, "key_loc.json"),"r"))

        item = item.replace("-"," ").replace("_", " ")

        if item in key_locs.keys():
            item_loc = key_locs[item]
        else:
            await ctx.send("Either that item doesn't exist or you need to ping aceynk.")
            return

        owned_amt = gk(ctx.author.id, item_loc)

        if int(amt) > owned_amt:
            await ctx.send("You can't gift more than you have.")
            return
        
        if not amt.isnumeric():
            await ctx.send("You need to provide a numeric amount to gift!")
            return
        
        if int(amt) < 0:
            await ctx.send("You can't gift negative items!")
            return
        
        ak(ctx.author.id, item_loc, -int(amt))
        ak(user.id, item_loc, int(amt))

        await ctx.send(f"Successfully traded **{int(amt)}** {item.title()} to *{user.display_name}*!")
        
            
    @commands.command(hidden=True)
    async def tooie(self,ctx):
        await ctx.send("hi tooie!")


    @commands.command(
        name="pronouns",
        aliases=["pronoun"],
        brief="Set your pronouns",
        help="Use !pronoun[s] <subject1>|<subject2>|<...>/<possessive1>|<possessive2>|<...>/<'have' conj.1>|<'have' conj.2>|<...> to set a list of pronouns for the bot to use.\nFor example, They|She/Their|Her/Have|Has is the correct form for they/them and she/her pronouns."
        )
    async def pronouns(self,ctx,pronounstr):
        sets = pronounstr.split("/")

        if len(sets) != 3:
            await ctx.send("I need you to provide info for all three sections!\nPersonal subject, personal possessive, and 'have' conjugations.\nUse !help pronouns for more info.")
            return

        sets = [x.split("|") for x in sets]

        if not (len(sets[0]) == len(sets[1]) == len(sets[2])):
            await ctx.send("You need to provide an equal amount of arguments for each section!\nUse !help pronouns for more info.")
            return
        
        sets = [[util.sanitize(y) for y in x] for x in sets]

        sk(ctx.author.id, "pronouns", {
            "subject": sets[0],
            "possessive": sets[1],
            "have": sets[2]
            })
        
        await ctx.send("Successfully set your pronouns! You should see them when people check your profile! :D")


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
        upgrade_bonus = [0,0,0,0]

        if "difficult_bait" in gk(self.id, "upgrades").keys():
            upgrade_bonus[0] = 10 * gk(self.id, ["upgrades","difficult_bait","amount"])
        if "challenging_bait" in gk(self.id, "upgrades").keys():
            upgrade_bonus[1] = 8 * gk(self.id, ["upgrades","challenging_bait","amount"])
        if "legendary_bait" in gk(self.id, "upgrades").keys():
            upgrade_bonus[2] = 6 * gk(self.id, ["upgrades","legendary_bait","amount"])
        if "special_bait" in gk(self.id, "upgrades").keys():
            upgrade_bonus[3] = 4 * gk(self.id, ["upgrades","special_bait","amount"])

        if "trash" in gk(self.id,"consumables").keys():
            trash_rec = min(475, gk(self.id,["consumables","trash","amount"]))

            return [
                950 - 2 * trash_rec,
                40 + trash_rec + upgrade_bonus[0],
                6 + trash_rec + upgrade_bonus[1],
                3 + upgrade_bonus[2],
                1 + upgrade_bonus[3]
                ]
        else:
            return [
                950,
                40 + upgrade_bonus[0],
                6 + upgrade_bonus[1],
                3 + upgrade_bonus[2],
                1 + upgrade_bonus[3]
                ]
        

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