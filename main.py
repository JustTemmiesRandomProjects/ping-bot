from http.client import HTTPException
import os
from dotenv import load_dotenv
import asyncio
import logging
from time import time, sleep
import random
import json
import glob

import discord
from discord.ext import tasks, commands

load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")

with open("config.json") as f:
    config = json.load(f)
    
owner_IDs = config["OWNER_IDS"]


channels = []


logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{time()}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

logging.error("error")
logging.critical("critical")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix = "--",
    owner_ids = [368423564229083137],
    intents = intents
)

@bot.event
async def on_ready():
    print("Loading cogs...")
    # loads cogs
    for filename in glob.iglob("./cogs/**", recursive=True):
        if filename.endswith('.py'):
            filename = filename[2:].replace("/", ".") # goes from "./cogs/economy.py" to "cogs.economy.py"
            await bot.load_extension(f'{filename[:-3]}') # removes the ".py" from the end of the filename, to make it into cogs.economy


    print(f"Logged in as {bot.user.name}")
    
    update_status.start()    
    update_channels.start()
    spam_task.start()

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@tasks.loop(minutes=10)
async def update_status():
    print("updating status")
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.listening, name="to pings"),
    )

@tasks.loop(minutes=30)
async def update_channels():
    print("updating cached channels")
    rawChannels = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            rawChannels.append(channel)
            sleep(0.005)

    channels.clear()
    for x, i in enumerate(rawChannels):
        if i.name.startswith("spam"):
            channels.append(i)
            
@tasks.loop(seconds=1)
async def spam_task():
    try:
        batch = random.sample(channels, random.randint(0, 3))
        coroutines = [channel.send("@everyone") for channel in batch]   
        await asyncio.gather(*coroutines)
    except Exception as e:
        print(f"rate limited {e}")
        spam_task.stop()
        return  


async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
