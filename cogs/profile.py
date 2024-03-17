# main impots
import discord

from discord.ext import commands

# local imports


class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="profile", aliases=["p"])
    async def fs_profile(self,ctx):
        pass



async def setup(bot):
    # init cog
    cog = profile(bot)
    await bot.add_cog(cog)