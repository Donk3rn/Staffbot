import discord
from discord.ext import commands
import asyncio
import os

# Intents: Viktig for å hente medlemsdata og roller
intents = discord.Intents.default()
intents.members = True  # Påkrevd for å hente alle medlemmer i roller
intents.guilds = True
intents.messages = True
intents.message_content = True  # Påkrevd for å lese kommandoer
intents.reactions = True

# Opprett bot med ønsket prefiks
bot = commands.Bot(command_prefix=".", intents=intents)

# Hendelse når boten er klar
@bot.event
async def on_ready():
    print(f"🔹 Botten er logget inn som {bot.user} (ID: {bot.user.id})")
    print("🔹 Botten er klar.")

# Laste inn alle cogs i ./cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"✅ Lastet cog: {filename}")

# Start bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start("DIN_DISCORD_BOT_TOKEN_HER")

# Kjør main loop
if __name__ == "__main__":
    asyncio.run(main())
