# main impots
import json
import os

import numpy as np

from discord.ext import commands

# local imports
import util
from .emoji import emoji

class fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="fish", aliases=["f","fishy","catch","cutes"])
    async def fs_fish(self,ctx):
        
        # get weight category
        cat_weight = [950,40,5,3,2]
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

        # await ctx.send(f"you caught a {catch['name']}")
        print(catch)

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

        emoji_output = f"{emoji().get_emoji(catch['name'])}"
        output = f"## Fishing Complete! 🎣\nYou caught a **{catch['name']}**\nPrice: {catch['price']}"

        if bonus:
            output += f"\n\nYou got bonus items!\n"
            bonus_set = set(bonus)

            for i in bonus_set:
                emoji_output += emoji().get_emoji(i)
                output += f"* {bonus.count(i)}x {i}\n"
            # await ctx.send(f"you caught bonus items!\n {bonus}")
                
            output = output[:-1]
                
        await ctx.send(output + "\n\n" + emoji_output)


async def setup(bot):
    # init cog
    cog = fishing(bot)
    await bot.add_cog(cog)