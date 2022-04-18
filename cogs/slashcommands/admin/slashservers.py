import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction

from essentials import BOT_OWNER_ID, GUILD_ID

class SlashServers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_if_is_is_me(interaction: Interaction):
        return interaction.user.id == BOT_OWNER_ID

    @nextcord.slash_command(name = "servers", description = "Admin command.", guild_ids = GUILD_ID)
    @application_checks.check(check_if_is_is_me)
    async def servers(self, interaction):
        activeservers = self.bot.guilds
        list = []
        i = 0
        for guild in activeservers:
            list.append("**" + guild.name + "**")
            i+=1

        return await interaction.send(f'Servers Names: {list}\n\nTotal Servers: **{i}**')

def setup(bot):
    bot.add_cog(SlashServers(bot))