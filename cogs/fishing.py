# main impots
import discord

from discord.ext import commands

# local imports


class fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="fish", aliases=["f","fishy","catch"])
    async def fs_fish(self,ctx):
        pass



async def setup(bot):
    # init cog
    cog = fishing(bot)
    await bot.add_cog(cog)