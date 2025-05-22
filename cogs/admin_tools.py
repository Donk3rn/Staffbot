import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta

ROLE_NAMES = {
    "Moderators": "Moderator",
    "Senior Moderators": "Senior Moderator",
    "Admins": "Admin",
    "Eier": "Eier"
}

class AdminTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def staff(self, ctx):
        class RoleSelector(discord.ui.View):
            def __init__(self, members):
                super().__init__(timeout=60)
                self.selected = []
                self.select = discord.ui.Select(
                    placeholder="Hvem skal unngås (Ja, Snip du kan velge fler)",
                    min_values=0,
                    max_values=len(members),
                    options=[
                        discord.SelectOption(label=member.display_name, value=str(member.id))
                        for member in members
                    ]
                )
                self.select.callback = self.select_callback
                self.add_item(self.select)

            async def select_callback(self, interaction: discord.Interaction):
                self.selected = self.select.values
                self.stop()

        class ModeSelector(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30)
                self.choice = None

                self.select = discord.ui.Select(
                    placeholder="VELG EN TING A IDIOT",
                    options=[
                        discord.SelectOption(label="Noen inhabil? Ja velg da", value="avoid"),
                        discord.SelectOption(label="Ikke unngå noen!", value="no_avoid")
                    ]
                )
                self.select.callback = self.select_callback
                self.add_item(self.select)

            async def select_callback(self, interaction: discord.Interaction):
                self.choice = self.select.values[0]
                self.stop()

        mode_view = ModeSelector()
        msg = await ctx.send("Velg en ting daaaa:", view=mode_view)
        await mode_view.wait()

        avoid_ids = []
        if mode_view.choice == "avoid":
            all_staff_members = set()
            for role_name in ROLE_NAMES.values():
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    all_staff_members.update(role.members)

            if not all_staff_members:
                return await ctx.send("Merker jeg ikke fant noen med staff roller.")

            avoid_view = RoleSelector(list(all_staff_members))
            avoid_msg = await ctx.send("Velg hvilke personer som skal ikke skal se ticketen:", view=avoid_view)
            await avoid_view.wait()

            await msg.delete()
            await avoid_msg.delete()

            confirm_msg = await ctx.send("✅ Ja det er registrert.")
            await discord.utils.sleep_until(datetime.utcnow() + timedelta(seconds=3))
            await confirm_msg.delete()

            avoid_ids = avoid_view.selected
        else:
            await msg.delete()
            confirm_msg = await ctx.send("✅ Jadaaa det er registrert.")
            await discord.utils.sleep_until(datetime.utcnow() + timedelta(seconds=3))
            await confirm_msg.delete()

        embed = discord.Embed(
            title="**PERME SØKNAD** Staff som er valgt ut",
            description="Disse er valgt til å lese søknader.",
            color=discord.Color.from_str("#00B7B3")
        )
        embed.set_footer(text=f"Dato: {datetime.now().strftime('%A %d.%m.%Y %H:%M')}")

        for title, role_name in ROLE_NAMES.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                continue
            members = [m for m in role.members if str(m.id) not in avoid_ids]
            count = 2 if title != "Eier" else 1
            chosen = random.sample(members, min(len(members), count)) if members else []
            lines = [f"{i+1}. {m.mention}" for i, m in enumerate(chosen)]
            embed.add_field(name=f"**{title}**", value="\n".join(lines) if lines else "Ingen valgt", inline=False)

        await ctx.send(embed=embed)

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
    await bot.add_cog(AdminTools(bot))
