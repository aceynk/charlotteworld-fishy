# main imports

from discord.ext import commands

# local imports
import util

#### cog ####
class emoji(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.EMOJI = {
            "Unknown": "❓",

            "Minnow": "🐟",
            "Halibut": "🐠",
            "Smelt": "🐟",

            "Salmon": "🐠",
            "Crab": "🦀",
            "Sea Nettle": "🪼",
            "Sardine": "🐟",

            "Squid": "🦑",
            "Rockfish": "🪨",

            "Swordfish": "🗡️",

            "Unique-Fish": "🐟",
            "Unique-Item": "⚔️",

            "Bottle": "🍾",
            "Boot": "🥾",
            "Tire": "🚗",
            "Cup": "🥤",
            "Plastic": "🎈",

            "Seaweed": "🌿",
            "Glistening Coin": "🪙",

            "Trout": "🐟",
            "Cod": "🐟",
            "Slug": "🐌",
            "Urchin": "🗯️",
            "Jellyfish": "🪼",
            "Ray": "🐟",
            "Shell": "🐚",

            "Shield": "🛡️",
            "Debris": "🪨",
            "Sword": "🗡️",
            "Clock": "🕐",
            "Knife": "🔪",
            "Key": "🔑"
        }


    def get_emoji(self, name):
        if name in self.EMOJI.keys():
            return self.EMOJI[name]
        if util.is_unique_fish(name):
            return self.EMOJI[name.split()[1]]
        if util.is_unique_item(name):
            return self.EMOJI[name.split()[1]]
        else:
            return self.EMOJI["Unknown"]
        
#### end cog ####
        
async def setup(bot):
    # init cog
    cog = emoji(bot)
    await bot.add_cog(cog)