import discord
from discord.ext import commands
import random
from datetime import datetime
import locale

# Sett norsk locale for ukedag hvis mulig
try:
    locale.setlocale(locale.LC_TIME, "nb_NO.UTF-8")
except:
    pass  # fallback til standard om systemet ikke støtter norsk

ROLE_NAMES = {
    "Moderators": "Moderator",
    "Senior Moderators": "Senior Moderator",
    "Admins": "Admin",
    "Administrator": "Administrator",
    "Eier": "Eier"
}


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def staff(self, ctx):
        class RoleSelector(discord.ui.View):
            def __init__(self, members, original_msg):
                super().__init__(timeout=120)
                self.selected = []
                self.original_msg = original_msg
                self.select = discord.ui.Select(
                    placeholder="Hvem skal ikke bli med (Ja Snip, du kan velge flere)",
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
                await interaction.message.delete()
                self.stop()

        class ModeSelector(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=90)
                self.choice = None

                self.select = discord.ui.Select(
                    placeholder="**JA NÅ MÅ DU VELGE!**",
                    options=[
                        discord.SelectOption(label="Noen du ikke vil ha med? TRYKK HER", value="avoid"),
                        discord.SelectOption(label="Ikke unngå noen", value="no_avoid")
                    ]
                )
                self.select.callback = self.select_callback
                self.add_item(self.select)

            async def select_callback(self, interaction: discord.Interaction):
                self.choice = self.select.values[0]
                await interaction.message.delete()
                self.stop()

        mode_view = ModeSelector()
        mode_msg = await ctx.send("JADA, VELG NÅ:", view=mode_view)
        await mode_view.wait()

        avoid_ids = []
        if mode_view.choice == "avoid":
            all_staff_members = set()
            for role_name in ROLE_NAMES.values():
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    all_staff_members.update(role.members)

            if not all_staff_members:
                return await ctx.send("Mashalla, fant ingen, noe er gærnt.")

            avoid_view = RoleSelector(list(all_staff_members), original_msg=mode_msg)
            avoid_msg = await ctx.send("Hvem skal ikke bli med? :", view=avoid_view)
            await avoid_view.wait()
            avoid_ids = avoid_view.selected

        # Dato-format: Torsdag 1.01.2011 - 00:00
        now = datetime.now()
        dato_tekst = now.strftime("Dato: %A %d.%m.%Y - %H:%M")
        embed = discord.Embed(
            title="**PERME SØKNAD** Staff som er valgt ut",
            description="Be Aasbu hente brillene, **Disse er valgt til å lese søknader.**",
            color=discord.Color.from_str("#00B7B3")
        )
        embed.set_footer(text=dato_tekst)

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


async def setup(bot):
    await bot.add_cog(Staff(bot))
