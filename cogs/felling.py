import discord
from discord.ext import commands

class Felling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def felling(self, ctx):
        legacy_role = discord.utils.get(ctx.guild.roles, name="Legacy")
        if not legacy_role:
            return await ctx.send("Fant ikke rollen **Legacy** på serveren.")

        # Hent medlemmer med rollen "Legacy"
        legacy_members = [m for m in ctx.guild.members if legacy_role in m.roles and not m.bot]

        if not legacy_members:
            return await ctx.send("Fant ingen medlemmer med rollen **Legacy**.")

        # View med dropdown for å velge én person
        class MemberSelector(discord.ui.View):
            def __init__(self, members):
                super().__init__(timeout=60)
                self.selected_id = None

                options = [
                    discord.SelectOption(label=member.display_name, value=str(member.id))
                    for member in members
                ]
                self.select = discord.ui.Select(
                    placeholder="Velg personen fellingen gjelder",
                    min_values=1,
                    max_values=1,
                    options=options
                )
                self.select.callback = self.select_callback
                self.add_item(self.select)

            async def select_callback(self, interaction: discord.Interaction):
                self.selected_id = int(self.select.values[0])
                await interaction.message.delete()
                self.stop()

        view = MemberSelector(legacy_members)
        msg = await ctx.send("Velg personen som fellingen gjelder:", view=view)
        await view.wait()

        if not view.selected_id:
            return await ctx.send("Ingen ble valgt.")

        member = ctx.guild.get_member(view.selected_id)

        await ctx.send(f"Heisann {member.mention}, her har du litt informasjon om fellingen din.")

        embed1 = discord.Embed(
            title="Felling – Fremgangsmåte",
            description=(
                "Vi oppretter en ticket der syv tilfeldige fra teamet blir valgt ut. "
                "Disse må være moderator, senior moderator, administrator eller eier.\n"
                "De utvalgte ser så på søknaden og tar en avgjørelse."
            ),
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
