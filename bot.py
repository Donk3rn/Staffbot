import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Logget inn som {bot.user}!")

# Last inn cogs
initial_extensions = ["cogs.staff", "cogs.felling"]

for ext in initial_extensions:
    bot.load_extension(ext)

# Start botten
bot.run(os.getenv("DISCORD_TOKEN"))
