# main imports
import discord

from discord.ext import commands

# local imports
import util
import botstate

### cog ###

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
            await self.bot.load_extension("cogs." + ext)
            print(f"Successfully loaded extensions {extensions}.")
            await ctx.send(f"Successfully loaded extensions {extensions}.")
    

    @commands.command(name="unload")
    @commands.check(util.is_mod)
    async def fs_unload(self,ctx,*extensions):
        for ext in extensions:
            await self.bot.unload_extension("cogs." + ext)
            print(f"Successfully unloaded extensions {extensions}.")
            await ctx.send(f"Successfully unloaded extensions {extensions}.")


    @commands.command(name="reload")
    @commands.check(util.is_mod)
    async def fs_reload(self,ctx,*extensions):
        for ext in extensions:
            await self.bot.reload_extension("cogs." + ext)
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


    @commands.command(name="untrust")
    @commands.check(util.is_mod)
    async def fs_untrust(self,ctx,member: discord.Member):
        trusted = botstate.get_key("trusted")
        trusted.remove(member.id)
        botstate.set_key("trusted",trusted)
        await ctx.send(f"Removed {member.name} from trusted users.")


    @commands.command(name="add_cogs")
    @commands.check(util.is_mod)
    async def fs_add_cogs(self,ctx,*cogs):
        cur_cogs = botstate.get_key("cogs")
        cur_cogs.extend(["cogs." + x for x in cogs])
        botstate.set_key("cogs",cur_cogs)

        for ext in cogs:
            await self.bot.load_extension("cogs." + ext)
        await ctx.send(f"Successfully loaded {cogs}.")


    @commands.command(name="remove_cogs")
    @commands.check(util.is_mod)
    async def fs_remove_cogs(self,ctx,*cogs):
        cur_cogs = botstate.get_key("cogs")
        for cog in cogs:
            cur_cogs.remove("cogs." + cog)
            await self.bot.unload_extension("cogs." + cog)
        
        botstate.set_key("cogs",cur_cogs)
        await ctx.send(f"Successfully unloaded {cogs}.")

### end cog ###

async def setup(bot):
    # init cog
    cog = dev(bot)
    await bot.add_cog(cog)