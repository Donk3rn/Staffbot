import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Logget inn som {bot.user}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
