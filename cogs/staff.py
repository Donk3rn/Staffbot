import discord
from discord.ext import commands
import random
from datetime import datetime
import locale

# Sett norsk locale for ukedag hvis mulig
try:
    locale.setlocale(locale.LC_TIME, "nb_NO.UTF-8")
except:
    pass  # fallback til manuell oversettelse

ROLE_NAMES = {
    "Moderators": "Moderator",
    "Senior Moderators": "Senior Moderator",
    "Admins": "Admin",
    "Administrator": "Administrator",
    "Eier": "Eier"
}

# Manuell fallback for ukedager på norsk
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
                discord.SelectOption(label="Ikke unngå noen", value="no_avoid"),
                discord.SelectOption(label="Ingen", value="none")
            ]
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        self.choice = self.select.values[0]
        await interaction.message.delete()
        if self.choice == "none":
            # Stopper uten å gjøre noe mer
            self.stop()
            return
        self.stop()

        # Trinn 1: Velg modus
        mode_view = ModeSelector()
        mode_msg = await ctx.send("Velg et alternativ:", view=mode_view)
        await mode_view.wait()

        try:
            await mode_msg.delete()
        except discord.NotFound:
            pass

        if not mode_view.choice:
            return  # Timeout

        # Trinn 2: Hent hvem som skal unngås (valgfritt)
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

            try:
                await avoid_msg.delete()
            except discord.NotFound:
                pass

            avoid_ids = avoid_view.selected

        # Trinn 3: Lag embed med valgt staff
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
                continue
            members = [m for m in role.members if str(m.id) not in avoid_ids]
            count = 2 if title != "Eier" else 1
            chosen = random.sample(members, min(len(members), count)) if members else []
            lines = [f"{i+1}. {m.mention}" for i, m in enumerate(chosen)]
            embed.add_field(name=f"**{title}**", value="\n".join(lines) if lines else "Ingen valgt", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Staff(bot))
