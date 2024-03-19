# main imports

from discord.ext import commands

# local imports

class emoji(commands.Cog):
    EMOJI = {
        "Unknown": "❓",

        "Minnow": "🐟",
        "Halibut": "🐠",
        "Smelt": "🐟",

        "Salmon": "🐟",
        "Crab": "🦀",
        "Sea Nettle": "🪼",

        "Squid": "🦑",

        "Swordfish": "🐠",

        "Unique-Fish": "🐟",
        "Unique-Item": "⚔️",

        "Bottle": "🍾",
        "Boot": "🥾",
        "Tire": "🚗",
        "Cup": "🥤",
        "Plastic": "🎈",

        "Seaweed": "🌿",
        "Glistening Coin": "🪙"
    }

    def get_emoji(self, name):
        if name in self.EMOJI.keys():
            return self.EMOJI[name]
        else:
            return self.EMOJI["Unknown"]
        
async def setup(bot):
    # init cog
    cog = emoji(bot)
    await bot.add_cog(cog)