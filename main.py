from http.client import HTTPException
import os
from dotenv import load_dotenv
import asyncio
import logging
from time import time, sleep
import random

import discord
from discord.ext import tasks, commands

load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")


role = "<@&994889021543166032>"
owner_IDs = [368423564229083137]


channels = []

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{time()}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

logging.error("error")
logging.critical("critical")

bot = commands.Bot(
    command_prefix = "--",
    owner_ids = owner_IDs,
    intents = discord.Intents.default()
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    
    update_channels.start()
    spam.start()

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def delete(ctx):
    guild = ctx.guild
    for category in guild.categories:
        try:
            await category.delete()
        except:
            pass

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

@bot.command()
async def startup(ctx):
    guild = ctx.guild
    for j in range(0, 10):
        try:
            await guild.create_category(name=f"spam {j+1}")
        except Exception as e:
            print(e)
            return
            
        for i in range(1, 51):
            try:
                channel = await guild.create_text_channel(f"spam-{j+1} - {i}", category=guild.categories[j])
                print("creating channel \"spam-{j+1}-{i}\"")
            except Exception as e:
                if e == HTTPException:
                    print("max channels reached")
                    break
                else:
                    print(f"error: {e}")
                    break

@tasks.loop(minutes=10)
async def update_status():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.listening, name="to pings"),
    )

@tasks.loop(minutes=5)
async def update_channels():
    rawChannels = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            rawChannels.append(channel)
            sleep(0.05)

    channels.clear()
    for x, i in enumerate(rawChannels):
        if i.name.startswith("spam"):
            channels.append(i)
            
@tasks.loop(seconds=2)
async def spam():
    try:
        batch = random.sample(channels, 45)
        coroutines = [channel.send(role) for channel in batch]   
        await asyncio.gather(*coroutines)
    except:
        print("rate limited")
        spam.stop()
        return


async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())