# main imports
import discord

from discord.ext import commands

# local imports
import util
import botstate

### start cog ###

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="set_prefix")
    @commands.check(util.is_mod)
    async def fs_set_prefix(self,ctx,prefix):
        botstate.set_key("prefix",prefix)
        await ctx.send(f"prefix set to {prefix}")


    @commands.command(name="load")
    @commands.check(util.is_mod)
    async def fs_load(self,ctx,*extensions):
        for ext in extensions:
            await self.bot.load_extension(ext)
            print(f"Successfully loaded extensions {extensions}.")
            await ctx.send(f"Successfully loaded extensions {extensions}.")
    

    @commands.command(name="unload")
    @commands.check(util.is_mod)
    async def fs_unload(self,ctx,*extensions):
        for ext in extensions:
            await self.bot.unload_extension(ext)
            print(f"Successfully unloaded extensions {extensions}.")
            await ctx.send(f"Successfully unloaded extensions {extensions}.")


    @commands.command(name="reload")
    @commands.check(util.is_mod)
    async def fs_reload(self,ctx,*extensions):
        for ext in extensions:
            await self.bot.reload_extension(ext)
            print(f"Successfully reloaded extensions {extensions}.")
            await ctx.send(f"Successfully reloaded extensions {extensions}.")


    @commands.command(name="end", aliases=["stop", "kill", "shutdown"])
    @commands.check(util.is_mod)
    async def fs_end(self,ctx):
        if ctx.message.content.startswith("!kill"):
            await ctx.send("You cannot kill me in a way that matters.")
        else:
            await ctx.send("Shutting down.")
        await self.bot.close()


    @commands.command(name="trust")
    @commands.check(util.is_mod)
    async def fs_trust(self,ctx,member: discord.Member):
        botstate.add_to_key("trusted",member.id)
        await ctx.send(f"Added {member.name} to trusted users.")

### end cog ###

async def setup(bot):
    # init cog
    cog = dev(bot)
    await bot.add_cog(cog)