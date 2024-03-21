# main impots
import json
import os
import random

import numpy as np

from discord.ext import commands

# local imports
import util
from .profile import gk,sk,ak

class fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="fish", aliases=["f","fishy","catch","cutes"])
    async def fs_fish(self,ctx):
        cur_profile = profile
        cur_profile.set_id(ctx.author.id)

        
        # get weight category
        cat_weight = cur_profile.get_base_weights()
        cats = ["normal","difficult","challenging","legendary","unique"]
        cat_weight /= np.sum(cat_weight)
        cat_choice = np.random.choice(cats,1,p=cat_weight)[0]

        # await ctx.send(f"you caught a {cat_choice} tier fish")

        # open fish json

        fishes = json.load(open(os.path.join(util.LOC,"fishes.json"),"r"))

        # get catch
        catch_weights = fishes[cat_choice]["weights"]
        catch_weights /= np.sum(catch_weights)
        catch = np.random.choice(fishes[cat_choice]["catches"],1,p=catch_weights)[0]

        print(catch)

        if not catch["name"] in [x["name"] for x in fishes["normal"]["catches"]]:
            cur_profile.clear_weight_bonus()

        if catch["name"] == "Unique-Fish":
            catch["name"] = util.get_unique_fish()
        if catch["name"] == "Unique-Item":
            catch["name"] = util.get_unique_item()

        # get bonus items
        bonus = []

        if "bonus" in catch.keys():
            item_list = catch["bonus"]["items"]
            item_list.append("Nothing")

            item_chances = catch["bonus"]["chances"]
            item_chances.append(1 - sum(item_chances))

            amount = catch["bonus"]["amount"]

            bonus.extend(np.random.choice(item_list,amount,replace=True,p=item_chances))

            print(f"bonus: {bonus}")

        
        # check for trash
        trashes = fishes["trash"]
        trashcount = len(trashes)
        trashes += ["Nothing"]

        bonus.extend(np.random.choice(trashes,5-cats.index(cat_choice),replace=True,p=(
            [0.01] * trashcount + [1 - 0.01 * trashcount]
        )))

        bonus = [x for x in bonus if x != "Nothing"]

        print(bonus)

        emoji_output = f"{emoji.get_emoji(catch['name'])}"
        output = f"## Fishing Complete! 🎣\nYou caught a **{catch['name']}**\nPrice: {catch['price']}"

        if bonus:
            output += f"\n\nYou got bonus items!\n"
            bonus_set = set(bonus)

            for i in bonus_set:
                emoji_output += (emoji.get_emoji(i)) * bonus.count(i)
                output += f"* {bonus.count(i)}x {i}\n"
                
            output = output[:-1]

        cur_profile.add_items(bonus)
        cur_profile.add_fish(catch["name"])
                
        await ctx.send(output + "\n\n" + emoji_output)

    @commands.command(name="recycle")
    async def fs_recycle(self,ctx,amount):
        cur_profile = profile
        cur_profile.set_id(ctx.author.id)

        rm_success = cur_profile.rm_random(
            json.load(open(os.path.join(util.LOC,"fishes.json"),"r"))["trash"],
            amount,
            ["items"])

        if rm_success:
            await ctx.send(f"Successfully recycled {rm_success} trash!")

            if "trash" in gk(ctx.author.id, "consumables").keys():
                ak(ctx.author.id, ["consumables","trash","amount"], rm_success)
            else:
                sk(ctx.author.id, ["consumables","trash"], {"amount": rm_success})
        else:
            await ctx.send(f"You don't have {amount} trash!")




async def setup(bot):
    # init cog
    cog = fishing(bot)

    global emoji
    global profile
    emoji = bot.get_cog("emoji")
    profile = bot.get_cog("profile")

    await bot.add_cog(cog)