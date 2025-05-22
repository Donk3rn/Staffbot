import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()  # Laster .env-fila
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Logget inn som {bot.user}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    await load_cogs()
    await bot.start(token)

asyncio.run(main())

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
