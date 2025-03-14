
---

## **5. `x42.py`**  
The main bot script.  
```python
import discord
import random
import requests
import asyncio
import os
from discord.ext import commands

TOKEN = os.getenv("TOKEN")  # Get from environment variables
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

def get_xkcd_comic(comic_id=None):
    """Fetch an XKCD comic by ID or get the latest one."""
    url = f"https://xkcd.com/{comic_id}/info.0.json" if comic_id else "https://xkcd.com/info.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"**{data['title']}**\n{data['img']}"
    return "Could not fetch XKCD comic."

@bot.command()
async def xkcd(ctx):
    """Post a random XKCD comic."""
    latest_comic = requests.get("https://xkcd.com/info.0.json").json()["num"]
    random_comic_id = random.randint(1, latest_comic)
    await ctx.send(get_xkcd_comic(random_comic_id))

@bot.command()
async def latest(ctx):
    """Post the latest XKCD comic."""
    await ctx.send(get_xkcd_comic())

async def daily_xkcd():
    """Posts the latest XKCD comic daily."""
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        await channel.send(get_xkcd_comic())  # Post latest XKCD
        await asyncio.sleep(86400)  # Wait 24 hours

async def random_xkcd():
    """Posts two random XKCD comics at random times within the day."""
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        await asyncio.sleep(random.randint(18000, 43200))  # Wait 5-12 hours
        latest_comic = requests.get("https://xkcd.com/info.0.json").json()["num"]
        random_comic_id = random.randint(1, latest_comic)
        await channel.send(get_xkcd_comic(random_comic_id))
        
        await asyncio.sleep(random.randint(18000, 43200))  # Wait 5-12 hours again
        random_comic_id = random.randint(1, latest_comic)
        await channel.send(get_xkcd_comic(random_comic_id))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(daily_xkcd())  # Start the daily latest comic task
    bot.loop.create_task(random_xkcd())  # Start the random comic task

bot.run(TOKEN)
