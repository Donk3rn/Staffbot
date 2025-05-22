import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

# Last inn miljøvariabler fra .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN ikke satt i .env-filen!")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

async def load_cogs():
    # Last inn dine cogs her. For eksempel 'staff.py' i 'cogs' mappen:
    await bot.load_extension("cogs.staff")

@bot.event
async def on_ready():
    print(f"Botten er logget inn som {bot.user}!")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
