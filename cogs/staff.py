import discord
from discord.ext import commands
import random
from datetime import datetime
import locale

try:
    locale.setlocale(locale.LC_TIME, "nb_NO.UTF-8")
except:
    pass

ROLE_NAMES = {
    "Moderators": "Moderator",
    "Senior Moderators": "Senior Moderator",
    "Admins": "Admin",
    "Administrator": "Administrator",
    "Eier": "Eier"
}

DAYS_NO = {
    "Monday": "Mandag",
    "Tuesday": "Tirsdag",
    "Wednesday": "Onsdag",
    "Thursday": "Torsdag",
    "Friday": "Fredag",
    "Saturday": "Lørdag",
    "Sunday": "Søndag"
}


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def staff(self, ctx):
        class RoleSelector(discord.ui.View):
            def __init__(self, members):
                super().__init__(timeout=120)
                self.selected = []
                self.select = discord.ui.Select(
                    placeholder="Velg hvem som skal unngås (kan velge flere)",
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
                    placeholder="Velg et alternativ",
                    options=[
                        discord.SelectOption(label="Unngå visse i staff", value="avoid"),
                        discord.SelectOption(label="Ikke unngå noen", value="no_avoid")
                    ]
                )
                self.select.callback = self.select_callback
                self.add_item(self.select)

            async def select_callback(self, interaction: discord.Interaction):
                self.choice = self.select.values[0]
                await interaction.message.delete()
                self.stop()

        # Første valg
        mode_view = ModeSelector()
        mode_msg = await ctx.send("Velg et alternativ:", view=mode_view)
        await mode_view.wait()

        if not mode_view.choice:
            try:
                await mode_msg.delete()
            except discord.NotFound:
                pass
            return

        avoid_ids = []
        if mode_view.choice == "avoid":
            all_staff_members = set()
            for role_name in ROLE_NAMES.values():
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    all_staff_members.update(role.members)

            if not all_staff_members:
                return await ctx.send("Fant ingen medlemmer i staff-roller.")

            avoid_view = RoleSelector(list(all_staff_members))
            avoid_msg = await ctx.send("Velg hvilke personer som skal unngås:", view=avoid_view)
            await avoid_view.wait()

            if not avoid_view.selected:
                try:
                    await avoid_msg.delete()
                except discord.NotFound:
                    pass
                return

            avoid_ids = avoid_view.selected

        # Formatert dato
        now = datetime.now()
        weekday_en = now.strftime("%A")
        weekday_no = DAYS_NO.get(weekday_en, weekday_en)
        dato_tekst = f"Dato: {weekday_no} {now.strftime('%d.%m.%Y - %H:%M')}"

        embed = discord.Embed(
            title="**PERME SØKNAD** Staff som er valgt ut",
            description="Disse er valgt til å lese søknader.",
            color=discord.Color.from_str("#00B7B3")
        )
        embed.set_footer(text=dato_tekst)

        for title, role_name in ROLE_NAMES.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                co
