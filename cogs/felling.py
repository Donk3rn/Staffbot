import discord
from discord.ext import commands

class Felling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def felling(self, ctx):
        embed1 = discord.Embed(
            title="Felling – Fremgangsmåte",
            description="Vi oppretter en ticket der fire tilfeldige fra teamet blir valgt ut. Disse må være senior moderator, administrator eller eier. De utvalgte ser så på søknaden og tar en avgjørelse.",
            color=discord.Color.from_str("#00B7B3")
        )

        embed2 = discord.Embed(
            title="Regler ved godkjent felling",
            description=(
                "Hvis du får godkjent felling gjelder følgende:\n\n"
                "- Din karakter må være den som setter nådestøtet.\n"
                "- Downes din karakter i scenarioet fellingen pågår, og du blør ut, er det din karakter som felles.\n"
                "- Du har 48 timer fra avgjørelsen faller til fellingen må utføres. Hvis personen ikke er logget inn kan du be om forlengelse.\n"
                "- Du MÅ gi beskjed i ticketen og i /report når scenarioet med fellingen starter. Du får beskjed om hvem du skal tagge.\n\n"
                "**Motpart vil ikke** få beskjed om fellingen før karakteren som skal felles har fått nådestøtet."
            ),
            color=discord.Color.from_str("#00B7B3")
        )

        embed3 = discord.Embed(
            description="Du hører fra oss!",
            color=discord.Color.from_str("#00B7B3")
        )
        embed3.set_footer(text="LEGACY ROLLESPILL", icon_url="https://i.vgy.me/rPbwfp.png")

        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)

async def setup(bot):
    await bot.add_cog(Felling(bot))
