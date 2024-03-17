# main imports
import discord
import random
import os

import asyncio as asy

from discord.ext import commands

# local imports
import util
import botstate

#### bot init ####

intents = discord.Intents.default()
intents.message_content = True

TOKEN = open(os.path.join(util.LOC,"botkey"),"r").read()

bot = commands.Bot(command_prefix=botstate.get_key("prefix"), intents=intents)

#### end bot init ####

#### helper functions ####

async def log_error(error):
    channel = bot.get_channel(1218730092436389899)
    await channel.send(error)

#### end helper functions ####

#### bot events ####

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # init cogs

    for i in botstate.get_key("cogs"):
        print(i)
        try:
            await bot.load_extension(i)
        except Exception as e:
            if isinstance(e, commands.ExtensionAlreadyLoaded):
                # if the extension is already loaded, it's a success lol
                continue
            print(f'Error loading {i}: {e}')

            # log error to channel
            await log_error(f"{i} failed to load with error: \n```\n{e}\n```")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    
    if isinstance(error, commands.CheckFailure):
        await ctx.send(random.choice(open("trustissues","r").readlines()))
    
    await log_error(f'{ctx.message.content}: ```\n{error}\n```')
    await ctx.send("An error occurred when running that command.")

#### end bot events ####
    
#### bot checks ####
    
@bot.check
async def no_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Sorry, this bot cannot be used in DMs.")
        return False
    return True

#### end bot checks ####

#### START BOT!! ####
    
bot.run(TOKEN)